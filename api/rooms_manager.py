from game.exceptions import ForbidenTransitionError
from typing import List, Optional, Dict
from game.Teams import TeamsEnum
from game.Teams import TeamsType
from game.GameState import GameState, Position
from starlette.websockets import WebSocket
import dataclasses
from random import choice
from starlette.websockets import WebSocketDisconnect
from api.helpers import get_game_state_from_json


@dataclasses.dataclass
class RoomInfo:
    exists: bool
    teams_joined: Optional[List[TeamsType]] = None


@dataclasses.dataclass
class Room:
    id: int
    red_ws: Optional[WebSocket]
    blue_ws: Optional[WebSocket]
    game_state: GameState
    steps_left: int = 2


class RoomsManager:
    def __init__(self) -> None:
        self.rooms: Dict[int, Room] = {}

    async def create_room(self, websocket: WebSocket, team):
        room_id = self.get_new_room_id()
        is_blue = team == TeamsEnum.BLUE.value
        self.rooms[room_id] = Room(
            id=room_id,
            blue_ws=websocket if is_blue else None,
            red_ws=websocket if not is_blue else None,
            game_state=GameState(h=8, w=8),
        )
        await self.send_state_update(
            websocket,
            {
                "roomId": room_id,
                "team": TeamsEnum.BLUE.value if is_blue else TeamsEnum.RED.value,
            },
        )
        return room_id

    async def join_room(self, room_id: int, websocket: WebSocket, team: int = None):
        room = self.rooms.get(room_id)
        if not room:
            await websocket.send_json(
                {"type": "error", "error": "room does not exist", "code": "RDNE"}
            )
            await websocket.close()
            return False
        if room.red_ws and room.blue_ws:
            await websocket.send_json(
                {"type": "error", "error": "room is already occupied", "code": "RIAO"}
            )
            await websocket.close()
            return False
        if room.red_ws and team == -1 or room.blue_ws and team == 1:
            await websocket.send_json(
                {"type": "error", "error": f"cant join as team {team}", "code": "CJAT"}
            )
            await websocket.close()
            return False

        join_as_red = (not team and not room.red_ws) or team == 1
        if join_as_red:
            room.red_ws = websocket
            if room.blue_ws:
                await self.send_state_update(
                    room.blue_ws, {"isOpponentConnected": True}
                )
        else:
            room.blue_ws = websocket
            await self.send_state_update(room.red_ws, {"isOpponentConnected": True})

        await self.send_state_update(
            websocket,
            {
                "roomId": room_id,
                "team": TeamsEnum.RED.value if join_as_red else TeamsEnum.BLUE.value,
                "isOpponentConnected": bool(room.blue_ws)
                if join_as_red
                else bool(room.red_ws),
            },
        )
        await self.reset_game_state_on_client(room_id, websocket)
        return True

    async def restart_room(self, room_id: int):
        room = self.rooms.get(room_id)
        if not room:
            return
        # Swap web sockets to play again with different color
        room.red_ws, room.blue_ws = room.blue_ws, room.red_ws
        room.game_state = GameState(8, 8)
        room.steps_left = 2
        await self.reset_from_server(room_id)

    def get_room_info(self, room_id: int) -> RoomInfo:
        room = self.rooms.get(room_id)
        if not room:
            return RoomInfo(exists=False)
        else:
            teams = []
            if room.red_ws:
                teams.append(-1)
            if room.blue_ws:
                teams.append(1)
            return RoomInfo(exists=True, teams_joined=teams)

    async def disconnect(self, room_id, websocket):
        print(self.rooms, room_id)
        room = self.rooms.get(room_id)
        print(room)
        if room.red_ws == websocket:
            room.red_ws = None
            if room.blue_ws:
                await self.send_state_update(
                    room.blue_ws, {"isOpponentConnected": False}
                )
        if room.blue_ws == websocket:
            room.blue_ws = None
            if room.red_ws:
                await self.send_state_update(
                    room.red_ws, {"isOpponentConnected": False}
                )
        if not room.red_ws and not room.blue_ws:
            del self.rooms[room_id]

    async def start_loop(self, room_id, websocket):
        try:
            while True:
                data = await websocket.receive_json()
                await self.handle(room_id, websocket, data)
        except WebSocketDisconnect:
            await self.disconnect(room_id, websocket)
            print("disconected")

    async def handle(self, room_id: int, websocket, data):
        if data["type"] == "move":
            await self.handle_move(room_id, websocket, data)

    async def handle_move(self, room_id: int, websocket, data):
        room = self.rooms[room_id]
        updated_state_frontend: GameState = get_game_state_from_json(data["state"])
        updated_state_backend: GameState = GameState.copy(room.game_state)
        updated_steps_left = room.steps_left
        for step in data["move"]:
            try:
                updated_state_backend.transition_single_cell(
                    Position(h=step[0], w=step[1])
                )
            except ForbidenTransitionError:
                print("forbiden transition")
                await self.initiate_recovery()
                return
            updated_steps_left -= 1
            if updated_steps_left == 0:
                updated_state_backend.to_move = -updated_state_backend.to_move
                updated_steps_left = 3

        if (
            not updated_state_backend.field == updated_state_frontend.field
            or not updated_state_backend.to_move == updated_state_frontend.to_move
            or not updated_steps_left == data["state"]["stepsLeft"]
        ):
            print("states do not match. Some error happened.")
            await self.reset_from_server(room_id)
            return
        # Now we established that the move is consistent.
        # Let's send it to the other player and update the state on the backend.
        is_blue = room.blue_ws == websocket

        if is_blue:
            await room.red_ws.send_json({"type": "move", "move": data["move"]})
        else:
            await room.blue_ws.send_json({"type": "move", "move": data["move"]})
        room.game_state = updated_state_backend
        room.steps_left = updated_steps_left

    def get_new_room_id(self):
        posible = set(range(1000, 10000))
        no_dups = posible.difference(set(self.rooms.keys()))
        return choice(list(no_dups))

    async def reset_from_server(self, room_id: int):
        room = self.rooms.get(room_id)
        if not room.red_ws and not room.blue_ws:
            print("trying to reset while one player is not connected")
            return
        await self.reset_game_state_on_client(room_id, room.red_ws, -1)
        await self.reset_game_state_on_client(room_id, room.blue_ws, 1)

    async def reset_game_state_on_client(
        self, room_id: int, websocket: WebSocket, team=None
    ):
        await websocket.send_json(
            {"type": "resetState", "field": self.rooms[room_id].game_state.field}
        )
        if team:
            await self.send_state_update(websocket, {"team": team})

    async def send_state_update(self, websocket: WebSocket, update):
        await websocket.send_json({"type": "stateUpdate", "state": update})

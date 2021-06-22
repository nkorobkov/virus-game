from fastapi import APIRouter, WebSocket, Request
from api.rooms_manager import RoomsManager

rooms_router = APIRouter()

manager = RoomsManager()


@rooms_router.websocket("/ws/room/")
async def create_room(websocket: WebSocket, team: int):
    await websocket.accept()
    room_id = await manager.create_room(websocket, team)
    await manager.start_loop(room_id, websocket)


@rooms_router.websocket("/ws/room/{room_id}")
async def join_room(websocket: WebSocket, room_id: int):
    await websocket.accept()
    success = await manager.join_room(room_id, websocket)
    print(success)
    if success:
        await manager.start_loop(room_id, websocket)


@rooms_router.get("/room/{room_id}/")
async def get_room_info(room_id: int):
    return manager.get_room_info(room_id)


@rooms_router.post("/room/{room_id}/restart")
async def restart_room(room_id: int):
    return await manager.restart_room(room_id)

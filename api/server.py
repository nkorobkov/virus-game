from api.helpers import get_game_state_from_text
from game.GameState import GameState
import asgiref.sync
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.evaluator.SimpleEvaluators import ActiveCountEvaluator
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

evaluator = ActiveCountEvaluator()
medium_engine = MiniMaxPolicy(evaluator, 2)

@app.websocket("/ws/ai/medium/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('accepted')
    try: 
        while True:
            text_data = await websocket.receive_text()
            game_state = get_game_state_from_text(text_data)           
            print('state received, finding a move')
            move = await asgiref.sync.sync_to_async(medium_engine.get_move)(game_state)
            await websocket.send_json({'move': move})
    except WebSocketDisconnect as exc:
        print('disconected')

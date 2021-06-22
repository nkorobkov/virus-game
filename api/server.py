import os
import asgiref.sync
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from minimax_policy.evaluator.SimpleEvaluators import ActiveCountEvaluator
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from starlette.websockets import WebSocketDisconnect

from api.helpers import get_game_state_from_json
from api.rooms_api import rooms_router

app = FastAPI()

app.include_router(rooms_router)


origins = [
    os.environ.get("ALLOWED_URL"),
    "https://localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


evaluator = ActiveCountEvaluator()
medium_engine = MiniMaxPolicy(evaluator, 2)


@app.websocket("/ws/ai/medium/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            game_state = get_game_state_from_json(data)
            print("state received, finding a move")
            move = await asgiref.sync.sync_to_async(medium_engine.get_move)(game_state)
            await websocket.send_json({"type": "move", "move": move})
    except WebSocketDisconnect:
        print("disconected")

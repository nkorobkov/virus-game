from Game.GameState import GameState
from Game.const import Position
from typing import List


class Engine:

    def get_move(self, game_state: GameState) -> List[Position]:
        raise NotImplementedError("Usage of get move from base Engine class")

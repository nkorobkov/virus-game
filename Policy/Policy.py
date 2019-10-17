from Game.GameState import GameState
from Game.const import Position
from typing import List


class Policy:
    name = 'baseclass'
    pos_checked = 0

    def get_move(self, game_state: GameState) -> List[Position]:
        raise NotImplementedError("Usage of get move from base Engine class")
from Game.GameState import GameState, Position
from typing import List, Tuple


class Policy:
    name = 'baseclass'
    pos_checked = 0

    def get_move(self, game_state: GameState) -> List[Position]:
        raise NotImplementedError("Usage of get move from base Engine class")


class EstimatingPolicy(Policy):

    def get_best_option(self, game_state: GameState) -> Tuple[float, List[Position]]:
        raise NotImplementedError("Usage of get best option from base Engine class")

    def get_move(self, game_state: GameState):
        return self.get_best_option(game_state)[1]

    def get_v(self, game_state: GameState):
        return self.get_best_option(game_state)[0]

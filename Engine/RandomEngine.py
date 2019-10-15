from Engine.Engine import Engine
from Game.GameState import GameState
from Engine.exceptions import *
from random import choice


class RandomEngine(Engine):

    def get_move(self, game_state: GameState):
        moves = list(game_state.get_all_moves())
        if not moves:
            raise NoValidMovesException("No move for {}".format(game_state.to_move))
        return choice(game_state.get_all_moves())

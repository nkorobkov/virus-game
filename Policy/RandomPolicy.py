from Policy.Policy import Policy
from Game.GameState import GameState
from Policy.exceptions import *
from random import choice


class RandomPolicy(Policy):
    name = 'Random'

    def get_move(self, game_state: GameState):
        moves = list(game_state.get_all_moves())
        if not moves:
            raise NoValidMovesException(game_state.to_move, 'No move for {}'.format(game_state.to_move))
        return choice(moves)

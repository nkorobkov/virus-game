from policy.Policy import EstimatingPolicy
from game.GameState import GameState
from policy.exceptions import *
from random import choice


class RandomPolicy(EstimatingPolicy):
    name = 'Random'


    def get_best_option(self, game_state:GameState):

        moves = list(game_state.get_all_moves())
        if not moves:
            raise NoValidMovesException(game_state.to_move, 'No move for {}'.format(game_state.to_move))
        return 0, choice(moves)
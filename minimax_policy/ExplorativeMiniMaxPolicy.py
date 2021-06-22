from game.GameState import GameState
from minimax_policy.evaluator import Evaluator
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from policy.exceptions import NoValidMovesException
from random import random, choice


class ExplorativeMiniMaxPolicy(MiniMaxPolicy):
    def __init__(self, evaluator: Evaluator, exploration_rate=0.1, depth=3):
        super().__init__(evaluator, depth)
        self.exploration_rate = exploration_rate
        self.name = "{}% Explorative ".format(self.exploration_rate * 100) + self.name

    def get_best_option(self, game_state: GameState):
        if random() < self.exploration_rate:
            moves = list(game_state.get_all_moves())
            if not moves:
                raise NoValidMovesException(for_team=game_state.to_move)
            return 0, choice(moves)
        return super().get_best_option(game_state)

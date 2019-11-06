from Game.GameState import GameState
from MiniMaxPolicy.Evaluator import Evaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from Policy.exceptions import NoValidMovesException
from random import random, choice


class ExplorativeMiniMaxPolicy(MiniMaxPolicy):
    def __init__(self, evaluator: Evaluator, exploration_rate=0.1, depth=3):
        super().__init__(evaluator, depth)
        self.exploration_rate = exploration_rate

    def get_best_option(self, game_state: GameState):
        if random() < self.exploration_rate:
            moves = list(game_state.get_all_moves())
            if not moves:
                raise NoValidMovesException(for_team=game_state.to_move)
            return 0, choice(moves)
        return super().get_best_option(game_state)

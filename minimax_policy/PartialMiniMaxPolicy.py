from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.evaluator import Evaluator
from typing import Callable
from random import sample


class PartialMiniMaxPolicy(MiniMaxPolicy):
    def __init__(
        self, evaluator: Evaluator, sample_size_resolver: Callable[[int], int], depth=3
    ):
        super().__init__(evaluator, depth)
        self.name = "Partial MiniMax with depth {} and evaluator {}".format(
            depth, evaluator.name
        )
        self.sample_size_resolver = sample_size_resolver

    def get_moves_to_check(self, game_state):
        # may want to change way of choosing later
        available_moves = list(game_state.get_all_moves())
        available_moves_count = len(available_moves)
        amount_to_check = min(
            available_moves_count, self.sample_size_resolver(available_moves_count)
        )
        return sample(available_moves, amount_to_check)

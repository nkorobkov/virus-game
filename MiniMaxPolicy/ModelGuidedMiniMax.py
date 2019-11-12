from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from Game.GameState import GameState
import torch.nn

from typing import Callable


class ModelGuidedMiniMax(ExplorativeMiniMaxPolicy):

    def __init__(self, model: torch.nn.Module, feature_extractor, h, w, evaluator,
                 sample_size_resolver: Callable[[int], int], exploration_rate=0, depth=3):
        super().__init__(evaluator, depth=depth, exploration_rate=exploration_rate)

        self.name = 'Guided MiniMax with depth {} and model {}'.format(depth, model.name)
        self.sample_size_resolver = sample_size_resolver
        self.model = model
        self.h = h
        self.w = w
        self.feature_extractor = feature_extractor

    def get_moves_and_states_to_check(self, game_state: GameState, depth: int):
        available_moves = list(game_state.get_all_moves())
        if not available_moves:
            return []
        available_moves_count = len(available_moves)
        amount_to_check = min(available_moves_count, self.sample_size_resolver(available_moves_count))
        next_states = [game_state.get_copy_with_move(move) for move in available_moves]

        if depth == 1:
            # next layer will use evaluator. It is faster (and better) to evaluate all states, than run a V estimation.
            return zip(available_moves, next_states)

        features_for_all_states = self.feature_extractor.get_features(next_states).float()
        v: torch.Tensor = self.model.forward(features_for_all_states)
        sorted_v, idx = v.sort(descending=False, dim=0)
        # we take n minimal values  for v on next state. Because model estimates value of position for moving player
        return [(available_moves[int(i)], next_states[int(i)]) for i in idx[:amount_to_check]]


if __name__ == '__main__':
    pass

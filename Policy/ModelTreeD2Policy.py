from typing import Tuple, List, Callable

import torch.nn

from Game.GameState import GameState, Move
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Policy.exceptions import NoValidMovesException
from random import random, choice


class ModelTreeD2Policy(ModelBasedPolicy):

    def __init__(self, model: torch.nn.Module, feature_extractor, h, w, sample_size_resolver: Callable[[int], int],
                 exploration=0, cuda=False):

        super().__init__(model, feature_extractor, h, w, exploration, cuda)
        self.name = 'Tree D2 and model {}'.format(model.name)
        self.sample_size_resolver = sample_size_resolver

    def get_state_value(self, game_state: GameState) -> float:
        available_moves, next_states, v = self.get_next_state_values(game_state)
        self.pos_checked += len(available_moves)
        return float(v.min())

    def get_best_option(self, game_state: GameState) -> Tuple[float, Move]:
        self.pos_checked = 0
        if random() < self.exploration:
            self.pos_checked = 0
            try:
                return 0, choice(list(game_state.get_all_moves()))
            except IndexError:
                raise NoValidMovesException(game_state.to_move)

        available_moves, next_states, values = self.get_next_state_values(game_state)
        sorted_v, idx = values.sort(descending=False, dim=0)
        amount_to_check = min(len(available_moves), self.sample_size_resolver(len(available_moves)))
        top_move, top_move_value = available_moves[0], -100
        for i in range(amount_to_check):
            cid = int(idx[i])
            move = available_moves[cid]
            state = next_states[cid]
            try:
                value = self.get_state_value(state)
            except NoValidMovesException:
                # after move oponent has no options. Means we just won.
                value = 100
                top_move = move
                break
            if value > top_move_value:
                top_move_value = value
                top_move = move

        return top_move_value, top_move

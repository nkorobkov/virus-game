from typing import Tuple, List, Callable

import torch.nn

from Game.GameState import GameState, Move
from Policy.Policy import EstimatingPolicy
from Policy.exceptions import NoValidMovesException
from random import random, choice


class ModelTreeD2Policy(EstimatingPolicy):

    def __init__(self, model: torch.nn.Module, feature_extractor, h, w, sample_size_resolver: Callable[[int], int],
                 exploration_rate=0):

        self.name = 'Model based Tree D2 and model {}'.format(model.name)
        self.sample_size_resolver = sample_size_resolver
        self.model = model
        self.h = h
        self.w = w
        self.feature_extractor = feature_extractor
        self.exploration_rate = exploration_rate

    def get_next_state_values(self, game_state: GameState):
        available_moves: List[Move] = list(game_state.get_all_moves())
        if not available_moves:
            raise NoValidMovesException(game_state.to_move, 'No move for {}'.format(game_state.to_move))
        next_states = [game_state.get_copy_with_move(move) for move in available_moves]
        features_for_all_states = self.feature_extractor.get_features(next_states).float()
        v: torch.Tensor = self.model.forward(features_for_all_states)
        return available_moves, next_states, v

    def get_state_value(self, game_state: GameState) -> float:
        available_moves, next_states, v = self.get_next_state_values(game_state)
        self.pos_checked +=len(available_moves)
        return float(v.min())

    def get_best_option(self, game_state: GameState) -> Tuple[float, Move]:
        self.pos_checked = 0
        if random() < self.exploration_rate:
            return 0, choice(list(game_state.get_all_moves()))

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
        #print(top_move)

        return top_move_value, top_move

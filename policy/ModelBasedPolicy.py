from typing import List

from game.GameState import GameState, Move
from policy.Policy import EstimatingPolicy
from policy.exceptions import *
import random
import numpy.random
import torch
import torch.cuda


class ModelBasedPolicy(EstimatingPolicy):
    def __init__(self, model, feature_extractor, h, w, exploration=0, cuda=False):
        self.model = model
        self.h = h
        self.w = w
        self.exploration = exploration
        self.feature_extractor = feature_extractor
        self.name = model.name
        self.cuda = cuda

    def get_next_state_values(self, game_state: GameState):
        available_moves, next_states = self.get_next_states(game_state)
        with torch.no_grad():
            features_for_all_states = self.feature_extractor.get_features(
                next_states
            ).float()
            if self.cuda:
                features_for_all_states = features_for_all_states.cuda()
            v: torch.Tensor = self.model.forward(features_for_all_states)
        return available_moves, next_states, v

    def get_next_states(self, game_state):
        available_moves: List[Move] = list(game_state.get_all_moves())
        if not available_moves:
            raise NoValidMovesException(
                game_state.to_move, "No move for {}".format(game_state.to_move)
            )
        next_states = [game_state.get_copy_with_move(move) for move in available_moves]
        return available_moves, next_states

    def get_best_option(self, game_state: GameState):
        available_moves, next_states, v = self.get_next_state_values(game_state)
        self.pos_checked = len(next_states)

        if self.exploration:
            if random.random() < self.exploration:
                v.squeeze_(1)
                v = v.numpy()
                v += abs(v.min())
                v /= v.sum()
                i = numpy.random.choice(range(len(available_moves)), p=v)
                return v[i], available_moves[i]

        # we minimize quality of position for moving player (opponent) prediction of the net for next state.
        best_move_value, best_move_index = v.min(0)
        # print(best_move_value)
        return best_move_value, available_moves[int(best_move_index)]

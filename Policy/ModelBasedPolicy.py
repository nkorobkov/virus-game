from Game.GameState import GameState
from Policy.Policy import EstimatingPolicy
from Policy.exceptions import *
from RL.Feature.KernelFeatures import KernelFeatureExtractor
import random
import numpy.random
import torch


class ModelBasedPolicy(EstimatingPolicy):

    def __init__(self, model, feature_extractor, h, w,exploration=0):
        self.model = model
        self.h = h
        self.w = w
        self.exploration = exploration

        self.feature_extractor = feature_extractor

        self.name = model.name

    def get_best_option(self, game_state: GameState):
        moves = list(game_state.get_all_moves())
        next_states = [game_state.get_copy_with_move(move) for move in moves]
        if not next_states:
            raise NoValidMovesException(game_state.to_move, 'No move for {}'.format(game_state.to_move))
        with torch.no_grad():
            features_for_all_states = self.feature_extractor.get_features(next_states).float()
            v: torch.Tensor = self.model.forward(features_for_all_states)

        self.pos_checked = len(next_states)

        if self.exploration:
            if random.random() < self.exploration:
                v.squeeze_(1)
                v = v.numpy()
                v += abs(v.min())
                v /= v.sum()
                i = numpy.random.choice(range(len(moves)), p=v)
                return v[i], moves[i]

        # we minimize quality of position for moving player (opponent) prediction of the net for next state.
        best_move_value, best_move_index = v.min(0)
        # print(best_move_value)
        return best_move_value, moves[int(best_move_index)]

from Game.GameState import GameState
from Policy.Policy import EstimatingPolicy
from Policy.exceptions import *
from RL.Feature.KernelFeatures import KernelFeatureExtractor
import random


class ModelBasedPolicy(EstimatingPolicy):

    def __init__(self, model, h, w, exploration=0):
        self.model = model
        self.h = h
        self.w = w
        self.exploration = exploration

        self.feature_extractor = KernelFeatureExtractor()

        self.name = model.name

    def get_best_option(self, game_state: GameState):
        moves = list(game_state.get_all_moves())
        next_states = [game_state.get_copy_with_move(move) for move in moves]
        if not next_states:
            raise NoValidMovesException(game_state.to_move, 'No move for {}'.format(game_state.to_move))

        features_for_all_states = self.feature_extractor.get_features(next_states).float()
        v = self.model.forward(features_for_all_states)

        if self.exploration:
            if random.random() > self.exploration:
                self.pos_checked = 1
                i = random.randint(0, v.shape[0] - 1)
                return v[i, 0], moves[i]

        self.pos_checked = len(next_states)

        if game_state.to_move == Teams.BLUE:
            best_move_value, best_move_index = v.max(0)
        else:
            best_move_value, best_move_index = v.min(0)
        # print(best_move_value)
        return best_move_value, moves[best_move_index]

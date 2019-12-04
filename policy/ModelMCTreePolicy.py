from typing import Tuple, List, Callable

import torch.nn

from game.GameState import GameState, Move
from policy.ModelBasedPolicy import ModelBasedPolicy
from policy.Policy import EstimatingPolicy
from policy.exceptions import NoValidMovesException
from random import random, choice


class ModelMCTreePolicy(ModelBasedPolicy):

    def __init__(self, model, feature_extractor, h, w, replays, exploration=0):
        super().__init__(model, feature_extractor, h, w, exploration)
        self.name = 'Monte-Carlo Tree and model {}'.format(model.name)
        self.replays = replays

    def get_best_option(self, game_state: GameState):
        pass




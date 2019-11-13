from typing import Tuple, List, Callable

import torch.nn

from Game.GameState import GameState, Move
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Policy.Policy import EstimatingPolicy
from Policy.exceptions import NoValidMovesException
from random import random, choice


class ModelMCTreePolicy(ModelBasedPolicy):

    def __init__(self, model, feature_extractor, h, w, replays, exploration=0):
        super().__init__(model, feature_extractor, h, w, exploration)
        self.name = 'Monte-Carlo Tree and model {}'.format(model.name)
        self.replays = replays

    def get_best_option(self, game_state: GameState):
        pass




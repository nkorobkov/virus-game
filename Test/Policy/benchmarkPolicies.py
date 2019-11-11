from time import time

from Policy.Policy import EstimatingPolicy, Policy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, ColoredCellsCountEvaluator
from Policy.RandomPolicy import RandomPolicy
from MiniMaxPolicy.Evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Game.GameState import GameState, Position
from Policy.exceptions import *
from Game.CellStates import *
from RL.Model.ConvolutionValue2 import ConvolutionValue2
from RL.Model.LinearValue import LinearValue
from RL.Model.SingleLayerValue import SingleLayerValue
from RL.Model.ThreeLayerValue import ThreeLayerValue
from RL.Model.ConvolutionValue import ConvolutionValue
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from Playground.util import readable_time_since
import cProfile
import torch

field = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -2, 0, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 2, -2, 2, 0, 0, 0, -1, 2, 2,
         0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, -1, 0, 0, 0, 1, 1, 0, 0, 0, -1]

game = GameState.from_field_list(8, 8, field, Teams.RED)

evaluatorActiveCells = ColoredCellsCountEvaluator()
policyAC = MiniMaxPolicy(evaluatorActiveCells, 1)
policyAC2 = MiniMaxPolicy(evaluatorActiveCells, 2)
policyAC2_r = ExplorativeMiniMaxPolicy(evaluatorActiveCells, 0.1, 2)

policy_random = RandomPolicy()

h, w = 8, 8

model = ConvolutionValue(h, w)
model.load_state_dict(torch.load('../../RL/learning/data/model8-conv-disc.pt'))
model.eval()
model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w)
model_guided30 = ModelGuidedMiniMax(model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 30, depth=3)

policies_to_evaluate = [policyAC, policyAC2, policyAC2_r, model_based, model_guided30]

for p in policies_to_evaluate:
    t = time()
    p.get_move(game)
    print('Policy: {} made move in {:.3f} sec.'.format(p.name, time() - t))

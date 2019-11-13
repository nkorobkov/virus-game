from time import time

from Policy.ModelTreeD2Policy import ModelTreeD2Policy
from Policy.Policy import EstimatingPolicy, Policy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, ActiveCountEvaluator
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
from random import choice

# in this position it is important to secure red base by stepping at 0 3, kill at 5 3  and add  extra life somewhere
# Ideal policy should do that.
field = [1, 0, 0, 0, 2, 0, 0, 0, 1, -1, -2, -2, 2, -1, -1, 0, 0, 1, 1, -2, 2, -1, 0, 0, 0, 1, -2, -2, 2, -1, -1, 0, 1,
         0, -2, -2, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 1, 0, -2, 2, -1, -1, 0, 0, 0, -2, -2, 2, 0, 0, -1]

# blue moves. It is important to unplug red's base to win. It is exact move.
field2 = [1, -1, 0, 0, 2, 0, 0, 0, 1, -1, -2, -2, 2, -1, -1, 0, 0, 1, 1, -2, 2, -1, 0, 0, 0, 1, -2, -2, 2, -1, -1, 0, 1,
          0, -2, -2, 2, 0, 0, 0, 0, 1, 1, -2, 2, 2, 0, 0, 0, 1, 0, -2, 2, -1, -1, 0, 0, -1, -2, -2, 2, 0, 0, -1]

game = GameState.from_field_list(8, 8, field, Teams.RED)
#game = GameState.from_field_list(8, 8, field2, Teams.BLUE)

game.print_field()

evaluatorActiveCells = ActiveCountEvaluator()
policyAC = MiniMaxPolicy(evaluatorActiveCells, 1)
policyAC2 = MiniMaxPolicy(evaluatorActiveCells, 2)
policyAC2_r = ExplorativeMiniMaxPolicy(evaluatorActiveCells, 0.1, 2)

policy_random = RandomPolicy()

h, w = 8, 8

model = ConvolutionValue(h, w)
model.load_state_dict(torch.load('../../RL/learning/data/model8-conv-disc2-10iz10.pt'))
model.eval()
model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w)
model_guided30 = ModelGuidedMiniMax(model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 50, depth=3)

model_tree = ModelTreeD2Policy(model, PlainFeatureExtractor(), h, w, lambda x: 30, 0.1)

policies_to_evaluate = [policy_random, policyAC, policyAC2, model_based,model_tree]

for p in policies_to_evaluate:
    t = time()
    p.get_move(game)
    print('Policy: {} made move in {:.3f} sec.'.format(p.name, time() - t))

t = time()
g = GameState()
moves = list(g.get_all_moves())
i = 0
while moves:
    g.make_move(choice(moves))
    moves = list(g.get_all_moves())
    i+=1

print('Played random game ({} moves) and determined random winner in {:.3f} sec.'.format(i, time() - t))

cProfile.run('model_tree.get_move(game)')

#
# def get_next_state_values(game_state, model):
#     available_moves = list(game_state.get_all_moves())
#     next_states = [game_state.get_copy_with_move(move) for move in available_moves]
#     features_for_all_states = PlainFeatureExtractor().get_features(next_states).float()
#     v: torch.Tensor = model.forward(features_for_all_states)
#     sorted_v, idx = v.sort(descending=False, dim=0)
#     return available_moves, next_states, sorted_v, idx
#
#
# available_moves, next_states, sorted_v, idx = get_next_state_values(game, model)
#
# for i in range(10):
#     print('{}th best move: V= {:.4f}'.format(i, float(sorted_v[i])))
#     print()
#     next_states[int(idx[int(i)])].print_field()
#     print(next_states[int(idx[int(i)])].field)
#
#     # _, nn_states, nn_v, nn_idx = get_next_state_values(next_states[int(idx[int(i)])], model)
#     # print('best  responce: V= {:.4f}'.format(float(nn_v[0])))
#     # nn_states[int(nn_idx[0])].print_field()
#
#     print()
#
# f = PlainFeatureExtractor().get_features([game.get_copy_with_move(policyAC2.get_move(game))]).float()
# print(model.forward(f))

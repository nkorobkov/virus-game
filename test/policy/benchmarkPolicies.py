from time import time

from policy.ModelTreeD2Policy import ModelTreeD2Policy
from policy.Policy import EstimatingPolicy, Policy
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from minimax_policy.ModelGuidedMiniMax import ModelGuidedMiniMax
from minimax_policy.evaluator.SimpleEvaluators import (
    MovableCountEvaluator,
    ActiveCountEvaluator,
)
from policy.RandomPolicy import RandomPolicy
from minimax_policy.evaluator.BidirectionalStepsWithWeightEval import (
    BidirectionalStepsWithWeightEval,
)
from policy.ModelBasedPolicy import ModelBasedPolicy
from game.GameState import GameState, Position
from policy.exceptions import *
from game.CellStates import *
from rl.model.ConvolutionValue2 import ConvolutionValue2
from rl.model.LinearValue import LinearValue
from rl.model.SingleLayerValue import SingleLayerValue
from rl.model.ThreeLayerValue import ThreeLayerValue
from rl.model.ConvolutionValue import ConvolutionValue
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor
from playground.util import readable_time_since
import cProfile
import torch
from random import choice

# in this position it is important to secure red base by stepping at 0 3, kill at 5 3  and add  extra life somewhere
# Ideal policy should do that.
field = [
    1,
    0,
    0,
    0,
    2,
    0,
    0,
    0,
    1,
    -1,
    -2,
    -2,
    2,
    -1,
    -1,
    0,
    0,
    1,
    1,
    -2,
    2,
    -1,
    0,
    0,
    0,
    1,
    -2,
    -2,
    2,
    -1,
    -1,
    0,
    1,
    0,
    -2,
    -2,
    2,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    2,
    2,
    0,
    0,
    0,
    1,
    0,
    -2,
    2,
    -1,
    -1,
    0,
    0,
    0,
    -2,
    -2,
    2,
    0,
    0,
    -1,
]

# blue moves. It is important to unplug red's base to win. It is exact move.
field2 = [
    1,
    -1,
    0,
    0,
    2,
    0,
    0,
    0,
    1,
    -1,
    -2,
    -2,
    2,
    -1,
    -1,
    0,
    0,
    1,
    1,
    -2,
    2,
    -1,
    0,
    0,
    0,
    1,
    -2,
    -2,
    2,
    -1,
    -1,
    0,
    1,
    0,
    -2,
    -2,
    2,
    0,
    0,
    0,
    0,
    1,
    1,
    -2,
    2,
    2,
    0,
    0,
    0,
    1,
    0,
    -2,
    2,
    -1,
    -1,
    0,
    0,
    -1,
    -2,
    -2,
    2,
    0,
    0,
    -1,
]

game = GameState.from_field_list(8, 8, field, Teams.RED)
# game = GameState.from_field_list(8, 8, field2, Teams.BLUE)

game.print_field()

evaluatorActiveCells = ActiveCountEvaluator()
policyAC = MiniMaxPolicy(evaluatorActiveCells, 1)
policyAC2 = MiniMaxPolicy(evaluatorActiveCells, 2)
policyAC2_r = ExplorativeMiniMaxPolicy(evaluatorActiveCells, 0.1, 2)

policy_random = RandomPolicy()

h, w = 8, 8

model = ConvolutionValue(h, w)
model.load_state_dict(torch.load("../../RL/learning/data/model8-conv-disc2-10iz10.pt"))
model.eval()
model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w)
model_guided30 = ModelGuidedMiniMax(
    model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 50, depth=3
)

model_tree = ModelTreeD2Policy(model, PlainFeatureExtractor(), h, w, lambda x: 30, 0.1)

policies_to_evaluate = [policy_random, policyAC, policyAC2, model_based, model_tree]

for p in policies_to_evaluate:
    t = time()
    p.get_move(game)
    print("Policy: {} made move in {:.3f} sec.".format(p.name, time() - t))

t = time()
g = GameState()
moves = list(g.get_all_moves())
i = 0
while moves:
    g.make_move(choice(moves))
    moves = list(g.get_all_moves())
    i += 1

print(
    "Played random game ({} moves) and determined random winner in {:.3f} sec.".format(
        i, time() - t
    )
)

cProfile.run("[model_tree.get_move(game) for _ in range(10)]")

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

import sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from minimax_policy.evaluator.SimpleEvaluators import ActiveCountEvaluator
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.ModelGuidedMiniMax import ModelGuidedMiniMax
from playground.play import play_with_policy
from policy.ModelBasedPolicy import ModelBasedPolicy
from policy.ModelTreeD2Policy import ModelTreeD2Policy
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor
from rl.model.ConvolutionValue import ConvolutionValue
from rl.model.ThreeLayerValue import ThreeLayerValue
import torch

h, w = 8, 8
model = ConvolutionValue(h, w)
model.load_state_dict(torch.load('../RL/learning/data/model8-conv-disc2-10iz10.pt'))
#model.load_state_dict(torch.load('../RL/learning/data/model8-second-gen-conv-15-1.pt'))
model.eval()

model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w, 0.)
model_tree = ModelTreeD2Policy(model, PlainFeatureExtractor(), h, w, lambda x: 30)

evaluatorActiveCells = ActiveCountEvaluator()
model_guided = ModelGuidedMiniMax(model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 30, depth=4)

play_with_policy(model_tree, h, w)

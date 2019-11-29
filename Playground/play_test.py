import sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from MiniMaxPolicy.Evaluator.SimpleEvaluators import ActiveCountEvaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from Playground.play import play_with_policy
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Policy.ModelTreeD2Policy import ModelTreeD2Policy
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from RL.Model.ConvolutionValue import ConvolutionValue
from RL.Model.ThreeLayerValue import ThreeLayerValue
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
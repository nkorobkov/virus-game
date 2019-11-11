from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from Playground.play import play_with_policy
from Policy.ModelBasedPolicy import ModelBasedPolicy
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from RL.Model.ConvolutionValue import ConvolutionValue
from RL.Model.ThreeLayerValue import ThreeLayerValue
import torch

h, w = 8, 8
model = ConvolutionValue(h, w)
model.load_state_dict(torch.load('../RL/learning/data/model8-conv-disc.pt'))
model.eval()

model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w, 0.)

evaluatorActiveCells = ColoredCellsCountEvaluator()
model_guided = ModelGuidedMiniMax(model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 100, depth=3)

play_with_policy(model_guided, h, w)
1
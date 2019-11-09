from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from Playground.play import play_with_policy
from Policy.ModelBasedPolicy import ModelBasedPolicy
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from RL.Model.ConvolutionValue import ConvolutionValue
from RL.Model.ThreeLayerValue import ThreeLayerValue
import torch

h, w = 5, 5
model = ConvolutionValue(h, w)
model.load_state_dict(torch.load('../RL/learning/data/model5-conv-disc.pt'))
model.eval()

model_based = ModelBasedPolicy(model, PlainFeatureExtractor(), h, w, 0.1)

evaluatorActiveCells = ColoredCellsCountEvaluator()

policyAC2 = MiniMaxPolicy(evaluatorActiveCells, 2)
model_guided = ModelGuidedMiniMax(model, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 410, depth=3)

play_with_policy(model_guided, h, w)

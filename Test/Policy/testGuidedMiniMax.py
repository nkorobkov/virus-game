from MiniMaxPolicy.Evaluator.SimpleEvaluators import *

from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from RL.Feature.KernelFeatures import KernelFeatureExtractor
from RL.Model.LinearValue import LinearValue
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestMimiMaxBasic(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        evaluator = ActiveCountEvaluator()
        model = LinearValue(3, 3)
        fe = KernelFeatureExtractor()
        self.policy = ModelGuidedMiniMax(model, fe, 3, 3, evaluator, lambda x: x // 2 + 1, depth=1)


if __name__ == '__main__':
    unittest.main()

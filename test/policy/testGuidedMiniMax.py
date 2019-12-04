from minimax_policy.evaluator.SimpleEvaluators import *

from minimax_policy.ModelGuidedMiniMax import ModelGuidedMiniMax
from rl.feature.KernelFeatures import KernelFeatureExtractor
from rl.model.LinearValue import LinearValue
from test.policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestGuidedMiniMax(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        evaluator = ActiveCountEvaluator()
        model = LinearValue(3, 3)
        fe = KernelFeatureExtractor()
        self.policy = ModelGuidedMiniMax(model, fe, 3, 3, evaluator, lambda x: x // 2 + 1, depth=1)


if __name__ == '__main__':
    unittest.main()

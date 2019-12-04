from minimax_policy.evaluator.SimpleEvaluators import *

from policy.ModelTreeD2Policy import ModelTreeD2Policy
from rl.feature.KernelFeatures import KernelFeatureExtractor
from rl.model.LinearValue import LinearValue
from test.policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestTree2D(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        model = LinearValue(3, 3)
        fe = KernelFeatureExtractor()
        self.policy = ModelTreeD2Policy(model, fe, 3, 3, lambda x: x // 2 + 1)


if __name__ == '__main__':
    unittest.main()

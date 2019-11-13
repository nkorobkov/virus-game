from MiniMaxPolicy.Evaluator.SimpleEvaluators import *

from Policy.ModelTreeD2Policy import ModelTreeD2Policy
from RL.Feature.KernelFeatures import KernelFeatureExtractor
from RL.Model.LinearValue import LinearValue
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestTree2D(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        model = LinearValue(3, 3)
        fe = KernelFeatureExtractor()
        self.policy = ModelTreeD2Policy(model, fe, 3, 3, lambda x: x // 2 + 1)


if __name__ == '__main__':
    unittest.main()

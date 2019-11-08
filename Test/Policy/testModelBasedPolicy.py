from Policy.ModelBasedPolicy import ModelBasedPolicy
from RL.Feature.KernelFeatures import KernelFeatureExtractor
from RL.Model.LinearValue import LinearValue
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestModelBasedPolicy(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        model = LinearValue(3, 3)
        self.policy = ModelBasedPolicy(model, KernelFeatureExtractor(), 3, 3)


if __name__ == '__main__':
    unittest.main()

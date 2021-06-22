from policy.ModelBasedPolicy import ModelBasedPolicy
from rl.feature.KernelFeatures import KernelFeatureExtractor
from rl.model.LinearValue import LinearValue
from test.policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestModelBasedPolicy(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        model = LinearValue(3, 3)
        self.policy = ModelBasedPolicy(model, KernelFeatureExtractor(), 3, 3)


if __name__ == "__main__":
    unittest.main()

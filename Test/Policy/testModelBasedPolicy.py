from Policy.ModelBasedPolicy import ModelBasedPolicy
from RL.Model.LinearValue import LinearValue
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestModelBasedPolicy(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        model = LinearValue(3, 3)
        self.policy = ModelBasedPolicy(model, 3, 3)


if __name__ == '__main__':
    unittest.main()

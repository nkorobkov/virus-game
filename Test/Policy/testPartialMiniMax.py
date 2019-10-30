from MiniMaxPolicy.Evaluator.SimpleEvaluators import *

from MiniMaxPolicy.PartialMiniMaxPolicy import PartialMiniMaxPolicy
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestMimiMaxBasic(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        evaluator = ColoredCellsCountEvaluator()
        self.policy = PartialMiniMaxPolicy(evaluator, lambda x: x // 2 + 1, 1)


if __name__ == '__main__':
    unittest.main()

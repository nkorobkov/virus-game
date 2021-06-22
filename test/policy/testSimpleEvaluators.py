from minimax_policy.evaluator.SimpleEvaluators import *
from test.policy.BaseEvaluatorTestCases import BaseCasesTests
import unittest


class TestColoredCellsCounterEvaluator(BaseCasesTests.BaseTestAnyEvaluator):
    def setUp(self):
        self.evaluator = ActiveCountEvaluator()

    def testNewField(self):
        game = GameState(5, 5)

        self.assertEqual(0, self.evaluator.evaluate(game))


class TestMovableCountEvaluator(BaseCasesTests.BaseTestAnyEvaluator):
    def setUp(self):
        self.evaluator = MovableCountEvaluator()


if __name__ == "__main__":
    unittest.main()

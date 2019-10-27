from MiniMaxPolicy.Evaluator.SimpleEvaluators import *
from Test.Policy.BaseEvaluatorTestCases import BaseCasesTests
import unittest


class TestColoredCellsCounterEvaluator(BaseCasesTests.BaseTestAnyEvaluator):

    def setUp(self):
        self.evaluator = ColoredCellsCountEvaluator()

    def testNewField(self):
        game = GameState(5, 5)

        self.assertEqual(0, self.evaluator.evaluate(game))

class TestMovableCountEvaluator(BaseCasesTests.BaseTestAnyEvaluator):

    def setUp(self):
        self.evaluator = MovableCountEvaluator()


if __name__ == '__main__':
    unittest.main()

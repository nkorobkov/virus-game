from MiniMaxPolicy.Evaluator.SimpleEvaluators import *
from MiniMaxPolicy.Evaluator.Evaluator import *
from Game.GameState import GameState, Field
from Game.const import *

import unittest

class BaseTestCases:

    class BaseTestAnyEvaluator(unittest.TestCase):
        evaluator = Evaluator()

        def testEmptyField(self):
            field: Field = [CellStates.EMPTY]
            game = GameState.from_field_list(1, 1, field, to_move=Teams.BLUE)

            self.assertEqual(0, self.evaluator.evaluate(game))

        @unittest.skip('not sure what behaviour to expect')
        def testNewField(self):
            game = GameState(5, 5)

            self.assertEqual(0, self.evaluator.evaluate(game))

        def testBlueDominates(self):
            field: Field = \
                [CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
                 CellStates.BB, CellStates.BA, CellStates.BB, CellStates.BB,
                 CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE,
                 CellStates.EE, CellStates.EE, CellStates.RB, CellStates.RA]

            game = GameState.from_field_list(4, 4, field, Teams.BLUE)
            self.assertTrue(self.evaluator.evaluate(game) > 0)

        def testRedDominates(self):
            field: Field = \
                [CellStates.RB, CellStates.EE, CellStates.RA, CellStates.EE,
                 CellStates.BB, CellStates.BA, CellStates.RA, CellStates.RB,
                 CellStates.BA, CellStates.RB, CellStates.EE, CellStates.EE,
                 CellStates.EE, CellStates.EE, CellStates.RB, CellStates.RA]

            game = GameState.from_field_list(4, 4, field, Teams.RED)
            self.assertTrue(self.evaluator.evaluate(game) < 0)


class TestColoredCellsCounterEvaluator(BaseTestCases.BaseTestAnyEvaluator):

    def setUp(self):
        self.evaluator = ColoredCellsCountEvaluator()

class TestMovableCountEvaluator(BaseTestCases.BaseTestAnyEvaluator):

    def setUp(self):
        self.evaluator = MovableCountEvaluator()



if __name__ == '__main__':
    unittest.main()
import unittest
from MiniMaxPolicy.Evaluator.Evaluator import *
from Game.GameState import GameState, Field
from Game.const import *


class BaseCasesTests:

    class BaseTestAnyEvaluator(unittest.TestCase):
        evaluator = Evaluator()

        def testEmptyField(self):
            field: Field = [CellStates.EMPTY]
            game = GameState.from_field_list(1, 1, field, to_move=Teams.BLUE)

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

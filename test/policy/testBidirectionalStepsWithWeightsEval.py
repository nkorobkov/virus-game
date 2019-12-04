from game.CellStates import CellStates
from game.Teams import Teams
from minimax_policy.evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from test.policy.BaseEvaluatorTestCases import BaseCasesTests
import unittest
from game.GameState import GameState, Field


class TestBasicScenarios(BaseCasesTests.BaseTestAnyEvaluator):

    def setUp(self):
        self.evaluator = BidirectionalStepsWithWeightEval()

    def testNewField(self):
        game = GameState(5, 5)

        self.assertEqual(0, self.evaluator.evaluate(game))


class TestExactValues(unittest.TestCase):

    def setUp(self):
        a, b, c, d, e = 2, 5, 9, 13, 17
        self.evaluator = BidirectionalStepsWithWeightEval(a, b, c, d)
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def testSimpleField(self):
        field: Field = \
            [CellStates.RB, CellStates.EE, CellStates.RA, CellStates.EE,
             CellStates.BB, CellStates.BA, CellStates.RA, CellStates.RB,
             CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.RB, CellStates.RA]

        game = GameState.from_field_list(4, 4, field, Teams.RED)
        expected_value_blue = 4 * self.a + 2 * self.b + 1 * self.c + 2 * self.d
        expected_value_red = - 6 * self.a - 2 * self.b - 3 * self.c - 3 * self.d

        self.assertEqual(expected_value_blue + expected_value_red, self.evaluator.evaluate(game))

    def testRealField(self):
        field: Field = \
            [CellStates.RA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE,
             CellStates.RB, CellStates.RA,
             CellStates.EE, CellStates.BB, CellStates.EE, CellStates.RA, CellStates.RB, CellStates.EE, CellStates.RB,
             CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.RB, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.RB,
             CellStates.EE, CellStates.EE,
             CellStates.BB, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.RB,
             CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.RB, CellStates.EE,
             CellStates.RA, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.BA, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.BA,
             CellStates.BA, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
             CellStates.EE, CellStates.BA]

        '''
        
         w\h |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |
        =====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
           0 |  ♘  |     | ♘♘♘ |     |     |  ♘  |     | ♘♘♘ |  ♘  |
             |     |     | ♘♘♘ |     |     |     |     | ♘♘♘ |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           1 |     | ♚♚♚ |     |  ♘  | ♘♘♘ |     | ♘♘♘ |     |     |
             |     | ♚♚♚ |     |     | ♘♘♘ |     | ♘♘♘ |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           2 |     |     | ♚♚♚ |     |     | ♚♚♚ |     | ♘♘♘ |     |
             |     |     | ♚♚♚ |     |     | ♚♚♚ |     | ♘♘♘ |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           3 |     | ♘♘♘ |     | ♚♚♚ | ♚♚♚ |     | ♘♘♘ |     |     |
             |     | ♘♘♘ |     | ♚♚♚ | ♚♚♚ |     | ♘♘♘ |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           4 | ♚♚♚ |  ♘  |     | ♚♚♚ |     | ♚♚♚ | ♘♘♘ |     |     |
             | ♚♚♚ |     |     | ♚♚♚ |     | ♚♚♚ | ♘♘♘ |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           5 |     |  ♘  |     | ♚♚♚ | ♘♘♘ |     |     | ♘♘♘ |     |
             |     |     |     | ♚♚♚ | ♘♘♘ |     |     | ♘♘♘ |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           6 |  ♘  |     | ♚♚♚ | ♚♚♚ | ♘♘♘ |     |     |  ♚  |     |
             |     |     | ♚♚♚ | ♚♚♚ | ♘♘♘ |     |     |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           7 |     | ♘♘♘ |     |     |  ♚  |     |  ♚  |  ♚  |     |
             |     | ♘♘♘ |     |     |     |     |     |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
           8 |     |     |  ♘  |     |     |     |  ♘  |     |  ♚  |
             |     |     |     |     |     |     |     |     |     |
        -----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
        
        
        aval repr for red: 40
        aval kills for red: 3
        Active bases for red:  10
        Active for Red: 9
        
        aval repr for blue: 29 
        aval kills for blue: 4
        Active bases for blue:  10
        Active for blue: 5        

        
        
        '''

        game = GameState.from_field_list(9, 9, field, Teams.RED)


        expected_value_blue = 29 * self.a + 4 * self.b + 10 * self.c + 5 * self.d
        expected_value_red = - 40 * self.a - 3 * self.b - 10 * self.c - 9 * self.d

        self.assertEqual(expected_value_blue + expected_value_red, self.evaluator.evaluate(game))



if __name__ == '__main__':
    unittest.main()

from MiniMaxPolicy.Evaluator.SimpleEvaluators import *
from MiniMaxPolicy.MiniMaxPolicy import *
from Game.GameState import GameState, Field, Position
from Game.CellStates import CellStates
from Game.Teams import Teams
from Test.Policy.BasePolicyTestCases import BaseCasesTests
import unittest


class TestMimiMaxBasic(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        evaluator = ActiveCountEvaluator()
        self.policy = MiniMaxPolicy(evaluator, 1)


class TestMiniMaxDepth1(unittest.TestCase):
    def setUp(self):
        evaluator = ActiveCountEvaluator()
        self.policy = MiniMaxPolicy(evaluator, 1)

    def testCanGetOnlyBase(self):
        field: Field = [CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSequenceEqual([Position(2, 1), Position(1, 2), Position(0, 3)], move)

    def testCanGetMaxBases1(self):
        field: Field = [CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA,
                        CellStates.EE, CellStates.RA, CellStates.EE, CellStates.EE,
                        CellStates.EE, CellStates.BA, CellStates.RA, CellStates.EE,
                        CellStates.RA, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSetEqual({Position(1, 1), Position(3, 0), Position(2, 2)}, set(move))

    def testCanGetMaxBases2(self):
        field: Field = [CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
                        CellStates.EE, CellStates.BA, CellStates.RA, CellStates.EE,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSetEqual({Position(1, 3), Position(0, 3), Position(2, 2)}, set(move))


class TestMiniMaxDepth2(unittest.TestCase):
    def setUp(self):
        evaluator = ActiveCountEvaluator()
        self.policy = MiniMaxPolicy(evaluator, 2)

    def testCanGetOnlyBase(self):
        field: Field = [CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSequenceEqual([Position(2, 1), Position(1, 2), Position(0, 3)], move)

    def testCanLock(self):
        field: Field = [CellStates.BB, CellStates.EE, CellStates.RA, CellStates.RA,
                        CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA,
                        CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSetEqual({Position(0, 2), Position(1, 2), Position(1, 3)}, set(move))

    def testCanLock2(self):
        field: Field = [CellStates.BB, CellStates.EE, CellStates.RA, CellStates.RA,
                        CellStates.EE, CellStates.BA, CellStates.RA, CellStates.RA,
                        CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.RB]

        game = GameState.from_field_list(4, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)

        self.assertSetEqual({Position(0, 2), Position(1, 2), Position(2, 2)}, set(move))

    def testCanChoseLockingOverBasingALot(self):
        field: Field = [CellStates.BA, CellStates.RB, CellStates.RA, CellStates.EE,
                        CellStates.BA, CellStates.RB, CellStates.EE, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
                        CellStates.RA, CellStates.RA, CellStates.EE, CellStates.EE]

        game = GameState.from_field_list(6, 4, field, Teams.BLUE)
        move = self.policy.get_move(game)
        # can make two based, but should make one and unplug red bases
        self.assertSetEqual({Position(2, 1), Position(1, 2), Position(0, 2)}, set(move))


if __name__ == '__main__':
    unittest.main()

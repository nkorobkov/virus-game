from policy.exceptions import *
from policy.Policy import Policy
from game.GameState import GameState, Field, Position
from game.CellStates import CellStates
from game.Teams import Teams

import unittest


class BaseCasesTests:
    class TestPolicyBasics(unittest.TestCase):
        def setUp(self):
            self.policy = Policy()

        def testPolicyReturnsMove(self):
            game = GameState(3, 3)
            move = self.policy.get_move(game)

            self.assertEqual(3, len(move))

        def testPolicyReturnsOnlyMove(self):
            field: Field = [
                CellStates.BA,
                CellStates.EE,
                CellStates.BB,
                CellStates.RB,
                CellStates.RB,
                CellStates.BB,
                CellStates.BB,
                CellStates.EE,
                CellStates.RA,
            ]

            game = GameState.from_field_list(3, 3, field, Teams.BLUE)
            move = self.policy.get_move(game)

            self.assertEqual(3, len(move))
            self.assertSequenceEqual(
                [Position(0, 1), Position(2, 2), Position(2, 1)], move
            )

        def testPolicyReturnsOnlyMoveForRed(self):
            field: Field = [
                CellStates.RA,
                CellStates.EE,
                CellStates.RB,
                CellStates.BB,
                CellStates.BB,
                CellStates.RB,
                CellStates.BB,
                CellStates.EE,
                CellStates.BA,
            ]

            game = GameState.from_field_list(3, 3, field, Teams.RED)
            move = self.policy.get_move(game)

            self.assertEqual(3, len(move))
            self.assertSequenceEqual(
                [Position(0, 1), Position(2, 2), Position(2, 1)], move
            )

        def testPolicyRaisesOnNoMove(self):
            field: Field = [
                CellStates.BA,
                CellStates.EE,
                CellStates.BB,
                CellStates.RB,
                CellStates.RB,
                CellStates.BB,
                CellStates.BB,
                CellStates.BB,
                CellStates.RA,
            ]

            game = GameState.from_field_list(3, 3, field, Teams.BLUE)
            with self.assertRaises(NoValidMovesException):
                self.policy.get_move(game)

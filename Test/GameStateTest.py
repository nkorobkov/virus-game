import unittest
from Game.GameState import GameState
from Game.const import CellStates, Teams


class TestGameSetup(unittest.TestCase):
    def testBasicInit(self):
        game = GameState()
        self.assertEqual(len(game.field), 100, "field size is default")
        self.assertEqual(game.field[0], CellStates.RED_ACTIVE, "red first dot set")
        self.assertEqual(game.field[-1], CellStates.BLUE_ACTIVE, "blue first dot set")

        self.assertEqual(game.size_w, 10, "sizew")
        self.assertEqual(game.size_h, 10, "sizeh")

        self.assertEqual(game.to_move, Teams.BLUE, "Move Blue")

    def testCustomSize(self):
        game = GameState(15)
        self.assertEqual(len(game.field), 15 ** 2, "field size is default")
        self.assertEqual(game.field[0], CellStates.RED_ACTIVE, "red first dot set")
        self.assertEqual(game.field[-1], CellStates.BLUE_ACTIVE, "blue first dot set")

        self.assertEqual(game.size_w, 15, "sizew")
        self.assertEqual(game.size_h, 15, "sizeh")

    def testCustomFieldSetup(self):
        pass


class TestUtils(unittest.TestCase):

    def testSetCell(self):
        pass


class TestNeighboursResolving(unittest.TestCase):
    pass


class TestSingleMovesResolving(unittest.TestCase):
    pass

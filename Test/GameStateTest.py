import unittest
from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams
from Game.Position import Position


class TestGameSetup(unittest.TestCase):
    def testBasicInit(self):
        game = GameState()
        self.assertEqual(len(game.field), 100, 'field size is default')
        self.assertEqual(game.field[0], CellStates.RED_ACTIVE, 'red first dot set')
        self.assertEqual(game.field[-1], CellStates.BLUE_ACTIVE, 'blue first dot set')

        self.assertEqual(game.size_w, 10, 'sizew')
        self.assertEqual(game.size_h, 10, 'sizeh')

        self.assertEqual(game.to_move, Teams.BLUE, 'Move Blue')

    def testCustomSize(self):
        game = GameState(15, 13)
        self.assertEqual(len(game.field), 195, 'field size is custom')

        self.assertEqual(game.field[0], CellStates.RED_ACTIVE, 'red first dot set')
        self.assertEqual(game.field[-1], CellStates.BLUE_ACTIVE, 'blue first dot set')
        self.assertEqual(game.field[50], CellStates.EMPTY, 'middle is empty')

        self.assertEqual(game.size_w, 13, 'sizew')
        self.assertEqual(game.size_h, 15, 'sizeh')

    def testCustomFieldSetup(self):
        field: Field = [CellStates.BLUE_ACTIVE, CellStates.BLUE_BASE, CellStates.BLUE_BASE, CellStates.RED_BASE,
                        CellStates.BLUE_ACTIVE, CellStates.EMPTY, CellStates.BLUE_BASE, CellStates.EMPTY,
                        CellStates.EMPTY, CellStates.RED_BASE, CellStates.RED_ACTIVE, CellStates.RED_ACTIVE]

        game = GameState.fromFieldList(3, 4, field, Teams.RED)

        self.assertEqual(len(game.field), 12, 'field size is as entered')
        self.assertEqual(game.size_w, 4)
        self.assertEqual(game.size_h, 3)
        self.assertEqual(game.field[0], CellStates.BLUE_ACTIVE, 'cells as defined')
        self.assertEqual(game.field[-1], CellStates.RED_ACTIVE, 'cells as defined')
        self.assertEqual(game.to_move, Teams.RED, 'team')
        self.assertEqual(game.field[1], CellStates.BLUE_BASE, 'cells as defined')
        self.assertEqual(game.field[-3], CellStates.RED_BASE, 'cells as defined')


class TestUtils(unittest.TestCase):

    def setUp(self):
        field: Field = [CellStates.BLUE_ACTIVE, CellStates.BLUE_BASE, CellStates.BLUE_BASE, CellStates.RED_BASE,
                        CellStates.BLUE_ACTIVE, CellStates.EMPTY, CellStates.BLUE_BASE, CellStates.EMPTY,
                        CellStates.EMPTY, CellStates.RED_BASE, CellStates.RED_ACTIVE, CellStates.RED_ACTIVE]

        self.game = GameState.fromFieldList(3, 4, field, Teams.RED)

    def testSetCell(self):
        self.game.set_cell(Position(1, 1), CellStates.BLUE_BASE)
        self.assertEqual(self.game.field[5], CellStates.BLUE_BASE)

    def testGetCellState(self):
        self.assertEqual(self.game.get_cell_state(Position(1, 1)), CellStates.EMPTY)
        self.assertEqual(self.game.get_cell_state(Position(0, 1)), CellStates.BLUE_BASE)
        self.assertEqual(self.game.get_cell_state(Position(2, 3)), CellStates.RED_ACTIVE)




class TestPositionConversions(unittest.TestCase):

    def setUp(self):
        self.game = GameState()

    def testIndexToPosition(self):
        self.assertEqual(self.game.index_to_position(0), Position(0, 0))
        self.assertEqual(self.game.index_to_position(3), Position(0, 3))
        self.assertEqual(self.game.index_to_position(10), Position(1, 0))
        self.assertEqual(self.game.index_to_position(11), Position(1, 1))
        self.assertEqual(self.game.index_to_position(20), Position(2, 0))
        self.assertEqual(self.game.index_to_position(9), Position(0, 9))
        self.assertEqual(self.game.index_to_position(99), Position(9, 9))

    def testPositionToIndex(self):
        self.assertEqual(self.game.position_to_index(Position(0, 0)), 0)
        self.assertEqual(self.game.position_to_index(Position(0, 1)), 1)
        self.assertEqual(self.game.position_to_index(Position(1, 0)), 10)
        self.assertEqual(self.game.position_to_index(Position(3, 4)), 34)
        self.assertEqual(self.game.position_to_index(Position(9, 9)), 99)
        self.assertEqual(self.game.position_to_index(Position(6, 0)), 60)

class TestNeighboursResolving(unittest.TestCase):
    pass

class TestSingleMovesResolving(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()

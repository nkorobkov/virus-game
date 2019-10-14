import unittest
from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams, Position


class TestGameSetup(unittest.TestCase):
    def testBasicInit(self):
        game = GameState()
        self.assertEqual(len(game.field), 100, 'field size is default')
        self.assertEqual(game.field[0], CellStates.BLUE_ACTIVE, 'red first dot set')
        self.assertEqual(game.field[-1], CellStates.RED_ACTIVE, 'blue first dot set')

        self.assertEqual(game.size_w, 10, 'sizew')
        self.assertEqual(game.size_h, 10, 'sizeh')

        self.assertEqual(game.to_move, Teams.BLUE, 'Move Blue')

    def testCustomSize(self):
        game = GameState(15, 13)
        self.assertEqual(len(game.field), 195, 'field size is custom')

        self.assertEqual(game.field[0], CellStates.BLUE_ACTIVE, 'red first dot set')
        self.assertEqual(game.field[-1], CellStates.RED_ACTIVE, 'blue first dot set')
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


class TestWithSimpleField(unittest.TestCase):

    def setUp(self):
        self.game = GameState()


class TestPositionConversions(TestWithSimpleField):

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


class TestNeighboursResolving(TestWithSimpleField):

    def testMiddleInd(self):
        pos = Position(5, 5)
        expected = {self.game.hw_to_index(4, 4), self.game.hw_to_index(4, 5), self.game.hw_to_index(4, 6),
                    self.game.hw_to_index(5, 4), self.game.hw_to_index(5, 6),
                    self.game.hw_to_index(6, 4), self.game.hw_to_index(6, 5), self.game.hw_to_index(6, 6)}

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(pos)), expected)

    def testCorner(self):
        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(9, 9))),
                            {self.game.hw_to_index(8, 9), self.game.hw_to_index(8, 8), self.game.hw_to_index(9, 8)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(0, 0))),
                            {self.game.hw_to_index(0, 1), self.game.hw_to_index(1, 1), self.game.hw_to_index(1, 0)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(0, 9))),
                            {self.game.hw_to_index(0, 8), self.game.hw_to_index(1, 8), self.game.hw_to_index(1, 9)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(9, 0))),
                            {self.game.hw_to_index(8, 0), self.game.hw_to_index(8, 1), self.game.hw_to_index(9, 1)})

    def testSide(self):
        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(5, 9))),
                            {self.game.hw_to_index(4, 9), self.game.hw_to_index(6, 9),
                             self.game.hw_to_index(4, 8), self.game.hw_to_index(5, 8), self.game.hw_to_index(6, 8)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(5, 0))),
                            {self.game.hw_to_index(4, 0), self.game.hw_to_index(6, 0),
                             self.game.hw_to_index(4, 1), self.game.hw_to_index(5, 1), self.game.hw_to_index(6, 1)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(0, 5))),
                            {self.game.hw_to_index(0, 4), self.game.hw_to_index(0, 6),
                             self.game.hw_to_index(1, 4), self.game.hw_to_index(1, 5), self.game.hw_to_index(1, 6)})

        self.assertSetEqual(set(self.game.get_cell_neighbours_indices(Position(9, 5))),
                            {self.game.hw_to_index(9, 4), self.game.hw_to_index(9, 6),
                             self.game.hw_to_index(8, 4), self.game.hw_to_index(8, 5), self.game.hw_to_index(8, 6)})


class TestSingleMovesResolving(unittest.TestCase):

    def testElementary(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, True, False,
             True, True, False,
             False, False, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'Elementary')

    def testBaseUsage(self):
        field: Field = \
            [CellStates.BA, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, False, True,
             True, True, True,
             False, False, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'base simple')

    def testBaseDeactevated(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.BB,
             CellStates.EE, CellStates.EE, CellStates.EE]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, True, False,
             True, True, False,
             False, False, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'base deact')

    def testBaseInfluence(self):
        field: Field = \
            [CellStates.BA, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.BB,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, False, True,
             True, True, False,
             False, True, True]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'base inf')

    def testPossibleMoves(self):
        field: Field = \
            [CellStates.BA, CellStates.BB, CellStates.EE,
             CellStates.RA, CellStates.BA, CellStates.EE,
             CellStates.RB, CellStates.EE, CellStates.EE]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, False, True,
             True, False, True,
             False, True, True]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'base possible moves')

    def testSubcomplexBlueMove(self):
        field: Field = \
            [CellStates.BA, CellStates.BA, CellStates.RA,
             CellStates.BA, CellStates.EE, CellStates.RB,
             CellStates.BA, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)

        expected: Mask = \
            [False, False, True,
             False, True, False,
             False, True, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected, 'subcomp')

    def testComplexRedMove(self):
        field: Field = \
            [CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
             CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA]

        game = GameState.fromFieldList(5, 5, field, Teams.RED)

        expected: Mask = \
            [False, True, False, True, False,
             False, True, False, True, False,
             False, True, False, True, False,
             False, True, True, True, False,
             False, False, True, False, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected)

    def testComplexBlueMove(self):
        field: Field = \
            [CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
             CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA]

        game = GameState.fromFieldList(5, 5, field, Teams.BLUE)

        expected: Mask = \
            [False, False, True, False, False,
             False, True, False, True, True,
             False, True, False, False, False,
             False, True, False, False, False,
             False, True, False, False, False]
        self.assertListEqual(game.get_all_single_moves_mask(), expected)


class TestIntermediateStepsMovesResolving(unittest.TestCase):
    maxDiff = None

    def testMaskToPositions(self):
        game = GameState(3, 3)
        mask: Mask = [True, False, False,
                      True, False, False,
                      False, False, True]
        positions = game.get_single_moves_positions_from_mask(mask)

        self.assertEqual(3, len(positions))
        self.assertSequenceEqual([Position(0, 0), Position(1, 0), Position(2, 2)], positions)

    def testDoubleMovesResolving(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        single_moves_mask: Mask = game.get_all_single_moves_mask()

        single_positions = game.get_single_moves_positions_from_mask(single_moves_mask)

        double_moves, second_to_firsts, first_to_seconds, seen_second_and_first_mask = \
            game.get_all_double_moves_from_single_moves(single_positions, single_moves_mask)

        expected = [[Position(h=0, w=1), Position(h=1, w=2)],
                    [Position(h=0, w=1), Position(h=0, w=2)],
                    [Position(h=1, w=0), Position(h=2, w=0)],
                    [Position(h=1, w=0), Position(h=2, w=1)],
                    [Position(h=1, w=1), Position(h=2, w=1)],
                    [Position(h=1, w=1), Position(h=2, w=2)],
                    [Position(h=1, w=1), Position(h=2, w=0)],
                    [Position(h=1, w=1), Position(h=1, w=2)],
                    [Position(h=1, w=1), Position(h=0, w=2)]]

        self.assertSequenceEqual(expected, double_moves)

    def test2StepMovesResolving(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        single_moves_mask: Mask = game.get_all_single_moves_mask()

        single_positions = game.get_single_moves_positions_from_mask(single_moves_mask)

        double_moves, second_to_firsts, first_to_seconds, seen_second_and_first_mask = \
            game.get_all_double_moves_from_single_moves(single_positions, single_moves_mask)

        # here we got move with duplicate single in both
        d_step_moves = list(game.get_all_ds_steps_moves(single_positions, second_to_firsts))

        expected = [(Position(h=0, w=1), Position(h=1, w=1), Position(h=1, w=2)),
                    (Position(h=0, w=1), Position(h=1, w=0), Position(h=1, w=2)),
                    (Position(h=1, w=1), Position(h=1, w=0), Position(h=1, w=2)),
                    (Position(h=0, w=1), Position(h=1, w=1), Position(h=0, w=2)),
                    (Position(h=0, w=1), Position(h=1, w=0), Position(h=0, w=2)),
                    (Position(h=1, w=1), Position(h=1, w=0), Position(h=0, w=2)),
                    (Position(h=1, w=0), Position(h=1, w=1), Position(h=2, w=0)),
                    (Position(h=1, w=0), Position(h=0, w=1), Position(h=2, w=0)),
                    (Position(h=1, w=1), Position(h=0, w=1), Position(h=2, w=0)),
                    (Position(h=1, w=0), Position(h=1, w=1), Position(h=2, w=1)),
                    (Position(h=1, w=0), Position(h=0, w=1), Position(h=2, w=1)),
                    (Position(h=1, w=1), Position(h=0, w=1), Position(h=2, w=1)),
                    (Position(h=1, w=1), Position(h=0, w=1), Position(h=2, w=2)),
                    (Position(h=1, w=1), Position(h=1, w=0), Position(h=2, w=2))]

        self.assertSequenceEqual(expected, d_step_moves)

    def test3StepMovesResolving(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RB,
             CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RB]

        game = GameState.fromFieldList(3, 4, field, Teams.BLUE)
        single_moves_mask: Mask = game.get_all_single_moves_mask()

        single_positions = game.get_single_moves_positions_from_mask(single_moves_mask)

        double_moves, second_to_firsts, first_to_seconds, seen_second_and_first_mask = \
            game.get_all_double_moves_from_single_moves(single_positions, single_moves_mask)

        t_step_moves = list(game.get_all_3_steps_moves(double_moves, single_moves_mask))

        expected = [(Position(h=0, w=1), Position(h=1, w=2), Position(h=0, w=3)),
                    (Position(h=0, w=1), Position(h=0, w=2), Position(h=0, w=3)),
                    (Position(h=1, w=1), Position(h=1, w=2), Position(h=0, w=3)),
                    (Position(h=1, w=1), Position(h=0, w=2), Position(h=0, w=3))]

        self.assertSequenceEqual(expected, t_step_moves)


class TestFullMovesResolving(unittest.TestCase):

    def moves_sanity_check(self, list_of_moves):
        move_set = set()
        for move in list_of_moves:
            # check no duplicates inside move
            if len(set(move)) != 3:
                return False
            move_set.add(tuple(sorted(move)))
        # check no duplicates
        return len(move_set) == len(list_of_moves)

    def testElementary(self):
        field: Field = \
            [CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.BA, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)
        # expect C(8,3)
        expected_num_of_moves = (8 * 7 * 6) / 6
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'Elementary')
        self.assertTrue(self.moves_sanity_check(moves))


    def testLimitedCorner(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # checked by hand
        expected_num_of_moves = 31
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'corner')
        self.assertTrue(self.moves_sanity_check(moves))

    def testFromBase(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)
        # C(7,3)
        expected_num_of_moves = 7 * 5
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'base center')
        self.assertTrue(self.moves_sanity_check(moves))

    def testEnemyBaseBlock(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # by hand
        expected_num_of_moves = 10
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'enemy base')
        self.assertTrue(self.moves_sanity_check(moves))

    def testNoMove(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.RB,
             CellStates.RB, CellStates.RB, CellStates.RB,
             CellStates.EE, CellStates.EE, CellStates.RA]

        game = GameState.fromFieldList(3, 3, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # by hand
        expected_num_of_moves = 0
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'no move')
        self.assertTrue(self.moves_sanity_check(moves))

    def testConnectionThroughBaseAfterFirst(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.EE]

        game = GameState.fromFieldList(1, 6, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # by hand
        expected_num_of_moves = 1
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'base conect 1')
        self.assertTrue(self.moves_sanity_check(moves))

    def testConnectionThroughBaseAfterSecond(self):
        field: Field = \
            [CellStates.BA, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.EE]

        game = GameState.fromFieldList(1, 6, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # by hand
        expected_num_of_moves = 1
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'base conect 2')
        self.assertTrue(self.moves_sanity_check(moves))


    def testConnectionThroughLayeredBase(self):
        field: Field = \
            [CellStates.BA, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE]

        game = GameState.fromFieldList(7, 7, field, Teams.BLUE)
        moves = list(game.get_all_moves())
        computed_num_of_moves = len(moves)

        # by hand
        expected_num_of_moves = 10+90+180+5*9*13
        self.assertEqual(expected_num_of_moves, computed_num_of_moves, 'base layered')
        self.assertTrue(self.moves_sanity_check(moves))

if __name__ == '__main__':
    unittest.main()

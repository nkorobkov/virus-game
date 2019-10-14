from Game.const import CellStates, Teams, Position
from collections import deque, defaultdict
from typing import List, Set, Iterator, Iterable, Tuple, DefaultDict, Dict, Any

from itertools import combinations, product, chain

from pprint import pprint

Mask = List[bool]
Field = List[CellStates]
Move = Tuple[Position, Position, Position]


class GameState:
    field: Field = []

    to_move: Teams = Teams.BLUE

    size_h = 0
    size_w = 0

    def __init__(self, h: int = 10, w: int = 10):
        self.size_h = h
        self.size_w = w
        self.field = [CellStates.EMPTY] * (h * w)

        self.set_cell(Position(0, 0), CellStates.BLUE_ACTIVE)
        self.set_cell(Position(h - 1, w - 1), CellStates.RED_ACTIVE)

    @classmethod
    def fromFieldList(cls, h: int, w: int, field: Field, to_move: Teams):
        if not h * w == len(field):
            raise AttributeError("field size does not match dimensions")
        game = GameState()
        game.size_h = h
        game.size_w = w
        game.field = field
        game.to_move = to_move
        return game

    def set_cell(self, pos: Position, state: CellStates):
        self.field[self.position_to_index(pos)] = state

    def get_cell_state(self, pos: Position) -> CellStates:
        return self.field[self.position_to_index(pos)]

    def hw_to_index(self, h, w) -> int:
        return h * self.size_w + w

    def position_to_index(self, pos) -> int:
        return self.hw_to_index(pos.h, pos.w)

    def index_to_position(self, index) -> Position:
        return Position(index // self.size_w, index % self.size_w)

    def is_single_cell_transition_possible(self, current_state, team):
        if not team == self.to_move:
            return False
        current_state.is_transition_possible(team)

    def transition_single_cell(self, pos: Position, team: Teams):

        # may be remove team and always use to move team

        current_state: CellStates = self.get_cell_state(pos)
        if self.is_single_cell_transition_possible(current_state, team):
            next_state = CellStates(current_state.after_move(team))
            self.set_cell(pos, next_state)

    def get_all_single_moves_mask(self) -> Mask:
        base_state = CellStates.BLUE_BASE if self.to_move == Teams.BLUE else CellStates.RED_BASE
        active_state = CellStates.BLUE_ACTIVE if self.to_move == Teams.BLUE else CellStates.RED_ACTIVE

        movable_mask: Mask = []
        reachable_mask: Mask = [False] * len(self.field)
        active_positions = deque()

        for i, cell in enumerate(self.field):
            movable_mask.append(cell.is_transition_possible(self.to_move))
            if cell == active_state:
                active_positions.append(self.index_to_position(i))

        active_bases_seen = set()
        while active_positions:
            p = active_positions.popleft()
            for cell_i in self.get_cell_neighbours_indices(p):
                state = self.field[cell_i]
                reachable_mask[cell_i] = True
                if state == base_state and cell_i not in active_bases_seen:
                    active_bases_seen.add(cell_i)
                    active_positions.append(self.index_to_position(cell_i))

        return [reachable and movable for reachable, movable in zip(reachable_mask, movable_mask)]

    def get_cell_neighbours_positions(self, pos):

        #   _____
        #  |* * .|
        #  |. = .|
        #  |. . .|
        #   '''''

        if pos.h > 0:
            yield Position(pos.h - 1, pos.w)
            if pos.w > 0:
                yield Position(pos.h - 1, pos.w - 1)
        #   _____
        #  |. . .|
        #  |. = .|
        #  |. * *|
        #   '''''

        if pos.h < self.size_h - 1:
            yield Position(pos.h + 1, pos.w)
            if pos.w < self.size_w - 1:
                #
                yield Position(pos.h + 1, pos.w + 1)

        if pos.w > 0:
            yield Position(pos.h, pos.w - 1)
            if pos.h < self.size_h - 1:
                yield Position(pos.h + 1, pos.w - 1)

        if pos.w < self.size_w - 1:
            yield Position(pos.h, pos.w + 1)
            if pos.h > 0:
                yield Position(pos.h - 1, pos.w + 1)

    def get_cell_neighbours_indices(self, pos):

        if pos.h > 0:
            yield self.hw_to_index(pos.h - 1, pos.w)
            if pos.w > 0:
                yield self.hw_to_index(pos.h - 1, pos.w - 1)

        if pos.h < self.size_h - 1:
            yield self.hw_to_index(pos.h + 1, pos.w)
            if pos.w < self.size_w - 1:
                #
                yield self.hw_to_index(pos.h + 1, pos.w + 1)

        if pos.w > 0:
            yield self.hw_to_index(pos.h, pos.w - 1)
            if pos.h < self.size_h - 1:
                yield self.hw_to_index(pos.h + 1, pos.w - 1)

        if pos.w < self.size_w - 1:
            yield self.hw_to_index(pos.h, pos.w + 1)
            if pos.h > 0:
                yield self.hw_to_index(pos.h - 1, pos.w + 1)

    def get_all_unseen_moves_from_pos(self, pos: Position, seen: Mask) -> Iterator[Position]:

        for index in self.get_cell_neighbours_indices(pos):
            if not seen[index] and self.field[index].is_transition_possible(self.to_move):
                yield self.index_to_position(index)

    def get_all_double_moves_from_single_moves(self, single_moves_positions: List[Position], single_moves_mask: Mask) \
            -> Tuple[List[Position], DefaultDict[Position, Set], DefaultDict[Position, List], Mask]:

        double_moves = []
        second_to_firsts = defaultdict(set)
        first_to_seconds = defaultdict(list)
        seen_second_and_first_mask: Mask = single_moves_mask.copy()

        for first_pos in single_moves_positions:
            for second_pos in self.get_all_unseen_moves_from_pos(first_pos, single_moves_mask):
                double_moves.append([first_pos, second_pos])
                seen_second_and_first_mask[self.position_to_index(second_pos)] = True
                second_to_firsts[second_pos].add(first_pos)
                first_to_seconds[first_pos].append(second_pos)
        return double_moves, second_to_firsts, first_to_seconds, seen_second_and_first_mask

    def get_all_3_steps_moves(self, double_moves, single_moves_mask:Mask) -> Iterator[Move]:
        for double_move in double_moves:
            third: Set[Position] = set()
            third.update(self.get_all_unseen_moves_from_pos(double_move[1], single_moves_mask))
            third.difference_update(self.get_all_unseen_moves_from_pos(double_move[0], single_moves_mask))
            yield from map(lambda y: (double_move[0], double_move[1], y), third)

    def get_all_ds_steps_moves(self, single_positions: List[Position], second_to_firsts) -> Iterable[Move]:
        '''
        :param single_positions: List of positions of  all reachable in one step cells
        :param second_to_firsts:
        :return: ierator of valid 3 cell moves that contains two cells reachable in  single step and one other
        '''
        for second, firsts in second_to_firsts.items():
            double_access = combinations(firsts, 2)
            rest = product(firsts, filter(lambda x: x not in firsts, single_positions))
            yield from map(lambda x: (x[0], x[1], second),
                           filter(lambda x: x[0] != x[1], chain(double_access, rest)))

    def get_all_dd_steps_moves(self, first_to_seconds: DefaultDict[Position, List[Position]]) ->Iterable[Move]:
        '''

        :param first_to_seconds:
        :return: iterator of valid 3 cell moves that contains one cell reachable in single step and two cells reachable
        in single step from it
        '''
        for first, seconds in first_to_seconds.items():
            yield from map(lambda x: (first, x[0], x[1]), combinations(seconds, 2))

    def get_single_moves_positions_from_mask(self, mask: Mask) -> List[Position]:
        single_positions = []
        for index, is_single_possible in enumerate(mask):
            if is_single_possible:
                single_positions.append(self.index_to_position(index))
        return single_positions

    def get_all_moves(self) -> Iterable[Move]:
        single_moves_mask: Mask = self.get_all_single_moves_mask()

        single_positions = self.get_single_moves_positions_from_mask(single_moves_mask)

        double_moves, second_to_firsts, first_to_seconds, seen_second_and_first_mask = \
            self.get_all_double_moves_from_single_moves(single_positions, single_moves_mask)

        t_step_moves = self.get_all_3_steps_moves(double_moves, single_moves_mask)

        dd_step_moves = self.get_all_dd_steps_moves(first_to_seconds)

        # here we got move with duplicate single in both
        d_step_moves = self.get_all_ds_steps_moves(single_positions, second_to_firsts)

        s_step_moves = combinations(single_positions, 3)

        return chain(t_step_moves, dd_step_moves, d_step_moves, s_step_moves)

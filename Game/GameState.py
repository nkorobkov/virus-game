from Game.CellStates import CellStates, CellStatesType
from Game.Teams import Teams, TeamsType
from collections import deque, defaultdict
from typing import List, Set, Iterator, Iterable, Tuple, DefaultDict, Dict
from Game.exceptions import *

from itertools import combinations, product, chain

from collections import namedtuple

# May be one day get rid of it and use only indices
Position = namedtuple('Position', ['h', 'w'])

Mask = List[bool]
MaskDict = Dict[TeamsType, Mask]
# Idea: use array of chars here from array module
Field = List[CellStatesType]
Move = Tuple[Position, Position, Position]


class GameState:
    field: Field = []

    to_move: TeamsType = Teams.BLUE

    size_h = 0
    size_w = 0

    def __init__(self, h: int = 10, w: int = 10, raw=False):
        self.size_h = h
        self.size_w = w
        self.field = [CellStates.EMPTY] * (h * w)

        self.set_cell(Position(0, 0), CellStates.BLUE_ACTIVE)
        self.set_cell(Position(h - 1, w - 1), CellStates.RED_ACTIVE)
        if not raw:
            self.movable_masks: MaskDict = self.get_movable_masks()
        else:
            self.movable_masks: MaskDict = None

    def __str__(self):
        return str(self.field)

    @classmethod
    def from_field_list(cls, h: int, w: int, field: Field, to_move: TeamsType):
        if not h * w == len(field):
            raise UnexpectedFieldSizeError("field size does not match dimensions")
        game = GameState(h, w)
        game.field = field
        game.to_move = to_move
        game.movable_masks = game.get_movable_masks()
        return game

    @classmethod
    def copy(cls, game):
        new_game = GameState(game.size_h, game.size_w, True)
        new_game.field = list(game.field)
        new_game.to_move = game.to_move
        new_game.movable_masks = game.copy_movable_masks()
        return new_game

    def copy_movable_masks(self) -> MaskDict:
        return {Teams.BLUE: list(self.movable_masks[Teams.BLUE]),
                Teams.RED: list(self.movable_masks[Teams.RED])}

    def set_cell(self, pos: Position, state: CellStatesType):
        self.field[self.position_to_index(pos)] = state

    def set_cell_on_index(self, index: int, state: CellStatesType):
        self.field[index] = state

    def get_cell_state(self, pos: Position) -> CellStatesType:
        return self.field[self.position_to_index(pos)]

    # numba
    def hw_to_index(self, h, w) -> int:
        return h * self.size_w + w

    # numba
    def position_to_index(self, pos) -> int:
        return self.hw_to_index(pos.h, pos.w)

    # numba
    def index_to_position(self, index) -> Position:
        return Position(index // self.size_w, index % self.size_w)

    def transition_single_cell(self, pos: Position):
        '''
        Changes the field like player self.to_move made a step at position pos
        :param pos:
        :return: None
        '''
        index = self.position_to_index(pos)
        current_state: CellStatesType = self.field[index]
        if self.movable_masks[self.to_move][index]:
            next_state = CellStates.after_transition(current_state, self.to_move)
            self.set_cell_on_index(index, next_state)
        else:
            raise ForbidenTransitionError(
                'transition on {} in state {} is not possible for  {}'.
                    format(pos, current_state, self.to_move))

    def update_movable_masks(self, move: Move) -> None:
        for to_move in [-1, 1]:
            for step in move:
                step_index = self.position_to_index(step)
                self.movable_masks[to_move][step_index] = CellStates.is_transition_possible(self.field[step_index],
                                                                                            to_move)

    def get_movable_masks(self) -> MaskDict:
        return \
            {to_move: list(map(lambda x: CellStates.is_transition_possible(x, to_move), self.field))
             for to_move in [1, -1]}

    def get_all_single_moves_mask(self) -> Tuple[Mask, Set[int]]:
        base_state = CellStates.BLUE_BASE if self.to_move == Teams.BLUE else CellStates.RED_BASE
        active_state = CellStates.BLUE_ACTIVE if self.to_move == Teams.BLUE else CellStates.RED_ACTIVE

        reachable_mask: Mask = [False] * len(self.field)
        active_positions = deque()

        for i, cell in enumerate(self.field):
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

        return [reachable and movable for reachable, movable in
                zip(reachable_mask, self.movable_masks[self.to_move])], active_bases_seen

    # consider nubma here
    def get_cell_neighbours_indices(self, pos: Position):
        h = pos.h
        w = pos.w
        if h > 0:
            yield self.hw_to_index(h - 1, w)
            if w > 0:
                yield self.hw_to_index(h - 1, w - 1)

        if h < self.size_h - 1:
            yield self.hw_to_index(h + 1, w)
            if w < self.size_w - 1:
                #
                yield self.hw_to_index(h + 1, w + 1)

        if w > 0:
            yield self.hw_to_index(h, w - 1)
            if h < self.size_h - 1:
                yield self.hw_to_index(h + 1, w - 1)

        if w < self.size_w - 1:
            yield self.hw_to_index(h, w + 1)
            if h > 0:
                yield self.hw_to_index(h - 1, w + 1)

    def get_all_unseen_moves_from_pos(self, pos: Position, seen: Mask, active_bases_already_seen: Set[int] = None) -> \
            Iterator[Position]:
        '''
        :param pos:
        :param seen:
        :param active_bases_already_seen: Function would not traverse bases that present in this set, to check
         if they lead to unseen move
        :return: Iterator on all positions that can be stepped from position pos, and have not been seen already
        (not in seen).
        '''
        base_state = CellStates.BLUE_BASE if self.to_move == Teams.BLUE else CellStates.RED_BASE
        if active_bases_already_seen is None:
            active_bases_seen = set()
        else:
            active_bases_seen: Set[int] = set(active_bases_already_seen)

        seen_this_run_indices = set()

        for index in self.get_cell_neighbours_indices(pos):
            if not seen[index] \
                    and self.movable_masks[self.to_move][index] \
                    and index not in seen_this_run_indices:
                # We can make a step at index position.
                seen_this_run_indices.add(index)
                yield self.index_to_position(index)

            elif self.field[index] == base_state and index not in active_bases_seen:
                # It is a base and we have not seen it before
                bases_to_check = deque([index])
                while bases_to_check:
                    checking_index = bases_to_check.popleft()
                    active_bases_seen.add(checking_index)
                    for checking_neighbour_index in self.get_cell_neighbours_indices(
                            self.index_to_position(checking_index)):
                        checking_neighbour_state = self.field[checking_neighbour_index]
                        if checking_neighbour_state == base_state and checking_neighbour_index not in active_bases_seen:
                            bases_to_check.append(checking_neighbour_index)
                        elif self.movable_masks[self.to_move][checking_neighbour_index] \
                                and checking_neighbour_index not in seen_this_run_indices \
                                and not seen[checking_neighbour_index]:
                            seen_this_run_indices.add(checking_neighbour_index)
                            yield self.index_to_position(checking_neighbour_index)

    def get_all_double_moves_from_single_moves(self, single_moves_positions: List[Position], single_moves_mask: Mask,
                                               active_bases_seen: Set[int]) \
            -> Tuple[List[List[Position]], DefaultDict[Position, Set], DefaultDict[Position, List]]:

        double_moves = []
        second_to_firsts = defaultdict(set)
        first_to_seconds = defaultdict(list)

        for first_pos in single_moves_positions:
            for second_pos in self.get_all_unseen_moves_from_pos(first_pos, single_moves_mask, active_bases_seen):
                double_moves.append([first_pos, second_pos])
                second_to_firsts[second_pos].add(first_pos)
                first_to_seconds[first_pos].append(second_pos)

        return double_moves, second_to_firsts, first_to_seconds

    def get_all_3_steps_moves(self, double_moves, single_moves_mask: Mask, initially_seen_active_bases: Set[int]) -> \
            Iterator[Move]:
        for double_move in double_moves:
            no_third: Set[Position] = set(
                self.get_all_unseen_moves_from_pos(double_move[0], single_moves_mask, initially_seen_active_bases))

            third: Set[Position] = set(
                self.get_all_unseen_moves_from_pos(double_move[1], single_moves_mask))
            # would  be nice to exclue bases seen on first move lookup somehow

            third.difference_update(no_third)
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

    def get_all_dd_steps_moves(self, first_to_seconds: DefaultDict[Position, List[Position]]) -> Iterable[Move]:
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
        single_moves_mask, active_bases_seen = self.get_all_single_moves_mask()

        single_positions = self.get_single_moves_positions_from_mask(single_moves_mask)

        double_moves, second_to_firsts, first_to_seconds = \
            self.get_all_double_moves_from_single_moves(single_positions, single_moves_mask, active_bases_seen)

        t_step_moves = self.get_all_3_steps_moves(double_moves, single_moves_mask, active_bases_seen)

        dd_step_moves = self.get_all_dd_steps_moves(first_to_seconds)

        # here we got move with duplicate single in both
        d_step_moves = self.get_all_ds_steps_moves(single_positions, second_to_firsts)

        s_step_moves = combinations(single_positions, 3)

        return chain(t_step_moves, dd_step_moves, d_step_moves, s_step_moves)

    def make_move(self, move):
        for pos in move:
            self.transition_single_cell(pos)
        self.to_move = Teams.other(self.to_move)
        self.update_movable_masks(move)

    def get_copy_with_move(self, move):
        new_state = GameState.copy(self)
        new_state.make_move(move)
        return new_state

    def print_field(self):

        header = ' w\h ' + '| {:3} ' * self.size_w + '|'
        header = header.format(*range(self.size_w))
        interm = '=====+' * (self.size_w + 1)
        line = '-----+' * (self.size_w + 1)
        print(header)
        print(interm)
        for i in range(self.size_h):
            print(' {:3} |'.format(i), end='')
            for j in range(self.size_w):
                print(' {:3} |'.format(CellStates.symbol(self.get_cell_state(Position(i, j)))), end='')
            print()
            print('     |', end='')
            for j in range(self.size_w):
                state = self.get_cell_state(Position(i, j))
                if state == CellStates.RED_ACTIVE or state == CellStates.BLUE_ACTIVE:
                    s = '   '
                else:
                    s = CellStates.symbol(state)
                print(' {:3} |'.format(s), end='')
            print()
            print(line)

from Game.const import CellStates, Teams
from Game.Position import Position
from collections import deque
from typing import List

Mask = List[bool]
Field = List[CellStates]


class GameState:
    field: Field = []

    to_move: Teams = Teams.BLUE

    size_h = 0
    size_w = 0

    def __init__(self, h: int = 10, w: int = 10):
        self.size_h = h
        self.size_w = w
        self.field = [CellStates.EMPTY] * (h * w)

        self.set_cell(Position(0, 0), CellStates.RED_ACTIVE)
        self.set_cell(Position(h - 1, w - 1), CellStates.BLUE_ACTIVE)

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
        #  |* = .|
        #  |. . .|
        #   '''''

        if pos.h > 0:
            yield Position(pos.h - 1, pos.w)
            if pos.w > 0:
                yield Position(pos.h, pos.w - 1)
                yield Position(pos.h - 1, pos.w - 1)
        #   _____
        #  |. . .|
        #  |. = *|
        #  |. * *|
        #   '''''

        if pos.h < self.size_h - 1:
            yield Position(pos.h + 1, pos.w)
            if pos.w < self.size_w - 1:
                yield Position(pos.h, pos.w + 1)
                yield Position(pos.h + 1, pos.w + 1)

        if pos.h < self.size_h - 1 and pos.w > 0:
            yield Position(pos.h + 1, pos.w - 1)

        if pos.h > 0 and pos.w < self.size_w - 1:
            yield Position(pos.h - 1, pos.w + 1)

    def get_cell_neighbours_indices(self, pos):

        if pos.h > 0:
            yield self.hw_to_index(pos.h - 1, pos.w)
            if pos.w > 0:
                yield self.hw_to_index(pos.h, pos.w - 1)
                yield self.hw_to_index(pos.h - 1, pos.w - 1)

        if pos.h < self.size_h - 1:
            yield self.hw_to_index(pos.h + 1, pos.w)
            if pos.w < self.size_w - 1:
                yield self.hw_to_index(pos.h, pos.w + 1)
                yield self.hw_to_index(pos.h + 1, pos.w + 1)

        if pos.h < self.size_h - 1 and pos.w > 0:
            yield self.hw_to_index(pos.h + 1, pos.w - 1)

        if pos.h > 0 and pos.w < self.size_w - 1:
            yield self.hw_to_index(pos.h - 1, pos.w + 1)

    def get_all_unseen_moves_from_cell(self, cell, seen: Mask):
        pass

    def get_all_moves(self):
        pass

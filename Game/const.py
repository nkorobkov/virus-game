import enum
from collections import namedtuple

CellState = namedtuple('CellState', ['blue_transition',
                                     'red_transition',
                                     'is_blue_transition_possible',
                                     'is_red_transition_possible',
                                     'team',
                                     'symbol'])

Position = namedtuple('Position', ['h', 'w'])

class Teams(enum.Enum):
    BLUE = 1
    RED = -1

    @property
    def other(self):
        return Teams(-self.value)


RED_BASE = CellState(None, None, False, False, Teams.RED, '♘♘♘')
BLUE_BASE = CellState(None, None, False, False, Teams.BLUE, '♚♚♚')
BLUE_ACTIVE = CellState(None, RED_BASE, False, True, Teams.BLUE, ' ♚ ')
RED_ACTIVE = CellState(BLUE_BASE, None, True, False, Teams.RED, ' ♘ ')
EMPTY = CellState(BLUE_ACTIVE, RED_ACTIVE, True, True, None, '   ')




class CellStates(enum.Enum):
    EMPTY: CellState = EMPTY
    BLUE_ACTIVE: CellState = BLUE_ACTIVE
    BLUE_BASE: CellState = BLUE_BASE
    RED_ACTIVE: CellState = RED_ACTIVE
    RED_BASE: CellState = RED_BASE

    EE: CellState = EMPTY
    BA: CellState = BLUE_ACTIVE
    BB: CellState = BLUE_BASE
    RA: CellState = RED_ACTIVE
    RB: CellState = RED_BASE

    @property
    def after_red_transition(self):
        return self.value.red_transition

    @property
    def after_blue_transition(self):
        return self.value.blue_transition

    @property
    def is_blue_transition_possible(self):
        return self.value.is_blue_transition_possible

    @property
    def is_red_transition_possible(self):
        return self.value.is_red_transition_possible

    @property
    def symbol(self):
        return self.value.symbol

    def is_transition_possible(self, team: Teams):
        if team == Teams.BLUE:
            return self.is_blue_transition_possible
        if team == Teams.RED:
            return self.is_red_transition_possible

    def after_transition(self, team: Teams):
        if team == Teams.BLUE:
            return self.after_blue_transition
        if team == Teams.RED:
            return self.after_red_transition


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

SYMBOLS = {
    -2: '♘♘♘',
    -1: ' ♘ ',
    0: '   ',
    1: ' ♚ ',
    2: '♚♚♚',
}


class CellStates(enum.Enum):
    EMPTY: CellState = 0
    BLUE_ACTIVE: CellState = 1
    BLUE_BASE: CellState = 2
    RED_ACTIVE: CellState = -1
    RED_BASE: CellState = -2

    BB: CellState = 2
    BA: CellState = 1
    EE: CellState = 0
    RA: CellState = -1
    RB: CellState = -2

    @property
    def symbol(self):
        return SYMBOLS[self.value]

    def is_transition_possible(self, team_val: int):
        t = self.value * team_val
        return t == 0 or t == -1

    def after_transition(self, team: Teams):
        '''
        Only  called with checked transition possible!
        Otherwise may return  wrong results
        :param team:
        :return:
        '''
        if self.value == 0:
            # if cell is empty, put an active there
            return team.value
        # if cell is not empty AND transition is possible (implied) than there should be a base of moving color
        return team.value * 2

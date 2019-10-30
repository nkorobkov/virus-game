CellStatesType = int


class CellStates:
    EMPTY: int = 0
    BLUE_ACTIVE: int = 1
    BLUE_BASE: int = 2
    RED_ACTIVE: int = -1
    RED_BASE: int = -2

    BB: int = 2
    BA: int = 1
    EE: int = 0
    RA: int = -1
    RB: int = -2

    SYMBOLS = {
        -2: '♘♘♘',
        -1: ' ♘ ',
        0: '   ',
        1: ' ♚ ',
        2: '♚♚♚',
    }

    @classmethod
    def is_transition_possible(cls, state: CellStatesType, team_val: int):
        t = state * team_val
        return t == 0 or t == -1

    @classmethod
    def after_transition(cls, state: CellStatesType, team: int) -> CellStatesType:
        '''
        Only  called with checked transition possible!
        Otherwise may return  wrong results
        :param team:
        :return:
        '''
        if state == 0:
            # if cell is empty, put an active there
            return team
        # if cell is not empty AND transition is possible (implied) than there should be a base of moving color
        return team * 2

    @classmethod
    def symbol(cls, state: CellStatesType):
        return cls.SYMBOLS[state]

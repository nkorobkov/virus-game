class InputDoesNotContainPosition(Exception):
    pass


class InputCanNotBeRecognized(Exception):
    pass


class MoveToPositionIsImpossible(Exception):
    def __init__(self, pos):
        self.position = pos


class GameInterruptedByUser(Exception):
    pass

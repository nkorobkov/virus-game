from Game.Teams import Teams


class NoValidMovesException(Exception):

    def __init__(self, for_team: Teams, msg=''):
        self.message = msg
        self.for_team = for_team

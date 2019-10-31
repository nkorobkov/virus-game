from Game.Teams import Teams, TeamsType


class NoValidMovesException(Exception):

    def __init__(self, for_team: TeamsType, msg=''):
        self.message = msg
        self.for_team = for_team

TeamsType = int


class Teams:
    BLUE = 1
    RED = -1

    @classmethod
    def other(cls, team):
        return -team

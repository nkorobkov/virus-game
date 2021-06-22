import enum

TeamsType = int


class TeamsEnum(enum.Enum):
    BLUE = 1
    RED = -1


class Teams:
    BLUE = 1
    RED = -1

    @classmethod
    def other(cls, team):
        return -team

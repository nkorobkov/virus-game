class Position:

    def __init__(self, h, w):
        self.h = h
        self.w = w

    def __eq__(self, other):
        return self.w == other.w and self.h == other.h

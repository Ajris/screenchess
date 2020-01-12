from enum import Enum

MOVES = [(1, 1), (1, -1)]


class Color(Enum):
    BLACK = -1
    WHITE = 1

    @property
    def moves(self):
        moves = map(lambda x: tuple([y*self.value for y in x]), MOVES)
        return list(moves)

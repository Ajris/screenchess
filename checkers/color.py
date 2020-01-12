from enum import Enum

possible_moves = [(1, 1), (1, -1)]


class Color(Enum):
    BLACK = -1
    WHITE = 1

    @property
    def moves(self):
        moves = map(lambda x: tuple([y*self.value for y in x]), possible_moves)
        return list(moves)

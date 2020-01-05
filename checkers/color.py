from enum import Enum

possible_moves = [(1, 1), (-1, 1)]

class Color(Enum):
    BLACK = -1
    WHITE = 1


    def find_possible_moves(self, row, column, board):
        new_possible_moves = map(lambda x: tuple([y*self.value for y in x]), possible_moves)
        print(new_possible_moves)

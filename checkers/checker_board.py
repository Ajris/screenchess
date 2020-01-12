from random import sample


class CheckerBoard:
    def __init__(self, board=None):
        self.board = [[None for _ in range(8)] for _ in range(8)] if board is None else board

    def set_piece(self, x, y, color):
        self.board[x][y] = color

    def valid_move(self, x, y):
        valid_range = x in range(7) and y in range(7)
        return valid_range and self.board[x][y] is None

    def find_moves(self, color):
        possible_moves = {}
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == color:
                    possible_moves[(row, column)] = [(row + x, column + y)
                                                     for (x, y) in color.moves
                                                     if self.valid_move(row + x, column + y)]
        return sample(possible_moves.items(), 1)

    def print_me(self):
        for i in range(8):
            for j in range(8):
                print(i, j, self.board[i][j])

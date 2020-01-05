from collections import defaultdict

WHITE = 1
BLACK = 2


class CheckerBoard:
    def __init__(self, board=None):
        self.board = [[0 for _ in range(8)] for _ in range(8)] if board is None else board

    def set_piece(self, x, y, piece):
        self.board[x][y] = piece

    def find_moves(self, piece):
        possible_moves = defaultdict(list)
        for column in self.board:
            for row in column:
                if self.board[column][row] == piece:
                    if piece == WHITE:
                        if (can_move(column + 1, row + 1)):
                            possible_moves[(column, row)].append((column + 1, row + 1))
                        elif can_move(column + 1, row - 1):
                            possible_moves[(column, row)].append((column + 1, row - 1))
                    elif piece == BLACK:
                        if (can_move(column - 1, row + 1)):
                            possible_moves[(column, row)].append((column - 1, row + 1))
                        elif can_move(column - 1, row - 1):
                            possible_moves[(column, row)].append((column - 1, row - 1))
    def can_move(self, x, y):
        pass
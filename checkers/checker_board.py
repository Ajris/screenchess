from collections import defaultdict


class CheckerBoard:
    def __init__(self, board=None):
        self.board = [[None for _ in range(8)] for _ in range(8)] if board is None else board

    def set_piece(self, x, y, color):
        self.board[x][y] = color

    def find_moves(self, color):
        possible_moves = defaultdict(list)
        for column in self.board:
            for row in column:
                if self.board[column][row].color == color:
                    moves = color.find_possible_moves(column, row, self.board)
                    possible_moves[(column, row)].append(moves)

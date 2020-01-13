from random import sample


class CheckerBoard:
    def __init__(self, board=None):
        self.board = [[None for _ in range(8)] for _ in range(8)] if board is None else board

    def set_piece(self, x, y, color):
        self.board[x][y] = color

    @staticmethod
    def valid_move_on_board(x, y):
        valid_range = x in range(7) and y in range(7)
        return valid_range

    def find_moves(self, color):
        possible_moves = {}
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == color:
                    possible_moves[(row, column)] = self.find_nearest_moves(color, row,
                                                                            column) + self.find_capture_moves(color,
                                                                                                              row,
                                                                                                              column)
        moves = [(x, y) for x, y in possible_moves.items() if y != []]
        return sample(moves, 1) if moves != [] else None

    def find_nearest_moves(self, color, row, column):
        return [(row + x, column + y)
                for x, y in color.moves
                if self.valid_move_on_board(row + x, column + y) and self.board[row + x][column + y] is None]

    def find_capture_moves(self, color, row, column):
        res = []
        for x, y in color.moves:
            if self.valid_move_on_board(row + 2 * x, column + 2 * y) and self.board[row + x][column + y] == -color.value:
                res += self.find_capture_moves(color, column + 2 * y, row + 2 * x) + [(row + 2 * x, column + 2 * y)]

        return res

    def print_me(self):
        for i in range(8):
            for j in range(8):
                print(i, j, self.board[i][j])

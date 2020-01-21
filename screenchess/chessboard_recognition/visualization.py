import cv2
from ..config import BOARD_DIM


def square_center(x, y, square_dim):
    return square_dim * y + square_dim // 2, square_dim * (BOARD_DIM - x) - square_dim // 2


def visualize_move(canvas, move):
    square_dim = canvas.shape[0] // BOARD_DIM
    start = square_center(move[0][0], move[0][1], square_dim)
    end = square_center(move[1][0], move[1][1], square_dim)
    return cv2.arrowedLine(canvas, start, end, (0, 255, 0), 4)

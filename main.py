import cv2
import crop_image
import chess
import numpy as np
import time
from checkers.checker_board import CheckerBoard
from checkers.color import Color
from recognize_chessboard import top_down_transform, find_markers
from clusterlist import ClusterList
from contextlib import contextmanager


@contextmanager
def camera(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()


def use_camera():
    count = 0
    with camera(0) as c:
        while 1:
            success, image = c.read()
            if success:
                cv2.imwrite(f'images/output/{count}.jpg', image)
                print(f'SAVED: {count}')
                count = count + 1
            else:
                break
            time.sleep(0.5)


def main():
    # useCamera()
    img = cv2.imread('images/input/test4.jpg')
    markers = find_markers(img)
    cluster = ClusterList(lambda x, y: np.linalg.norm(x - y) < 40,
                          lambda x, y: ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2))
    for point in markers:
        cluster.append(point[0])
    warped = top_down_transform(img, np.array(cluster.data))
    checker_board = CheckerBoard()
    board = chess.Board(None)
    for position, color in crop_image.find_pieces(warped):
        checker_board.set_piece(position//8, position%8, color)
        # board.set_piece_at(position, chess.Piece(chess.PAWN, color))
    # return board.fen()
    print(checker_board.board)
    checker_board.find_moves(Color.WHITE)


if __name__ == '__main__':
    print(main())

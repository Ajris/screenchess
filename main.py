import cv2
import numpy as np
from checkers.checker_board import CheckerBoard
from checkers.color import Color
from contextlib import contextmanager
from chessboard_recognition import crop_image, recognize_chessboard, clusterlist


@contextmanager
def camera(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()


def main():
    # useCamera()
    img = cv2.imread('images/input/lol2.jpg')
    markers = recognize_chessboard.find_markers(img)
    cluster = clusterlist.ClusterList(lambda x, y: np.linalg.norm(x - y) < 40,
                                      lambda x, y: ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2))
    for point in markers:
        cluster.append(point[0])
    cluster.trim(5)
    warped = recognize_chessboard.top_down_transform(img, np.array(cluster.data))
    checker_board = CheckerBoard()
    for position, color in crop_image.find_pieces(warped):
        checker_board.set_piece(position//8, position%8, color)
    # print(checker_board.board)
    checker_board.print_me()
    move = checker_board.find_moves(Color.BLACK)
    print(move)


if __name__ == '__main__':
    main()

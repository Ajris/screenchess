import cv2
import crop_image
import chess
import numpy as np
import time
from recognize_chessboard import top_down_transform, find_markers
from clusterlist import ClusterList

from contextlib import contextmanager

@contextmanager
def VideoCapture(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()

def main():
    count = 0
    with VideoCapture(0) as c:
        while 1:
            success, image = c.read()
            if success:
                cv2.imwrite(f'images/output/{count}.jpg', image)
                print(f'SAVED: {count}')
                count = count + 1
            else:
                break
            time.sleep(0.5)

    img = cv2.imread('images/input/test4.jpg')
    markers = find_markers(img)
    cluster = ClusterList(lambda x, y: np.linalg.norm(x - y) < 40)
    for point in markers:
        cluster.append(point[0])
    warped = top_down_transform(img, np.array(cluster.data))
    board = chess.Board(None)
    for position, color in crop_image.find_pieces(warped):
        board.set_piece_at(position, chess.Piece(chess.PAWN, color))
    return board.fen()


if __name__ == '__main__':
    print(main())

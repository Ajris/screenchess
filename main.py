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

# def use_camera():
#     count = 0
#     with camera(0) as c:
#         while 1:
#             success, image = c.read()
#             if success:
#                 cv2.imwrite(f'images/output/{count}.jpg', image)
#                 print(f'SAVED: {count}')
#                 count = count + 1
#                 # recognize_img(image, count)
#             else:
#                 break
#             # time.sleep(2)

def main():
    # useCamera()
    img = cv2.imread('images/input/test.jpg')
    markers = recognize_chessboard.find_markers(img)
    cluster = clusterlist.ClusterList(lambda x, y: np.linalg.norm(x - y) < 40,
                                      lambda x, y: ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2))
    for point in markers:
        cluster.append(point[0])
    cluster.trim(5)
    for i in cluster:
        print(i, type(i))
    print(cluster.data)
    warped = recognize_chessboard.top_down_transform(img, np.array(cluster.data))
    checker_board = CheckerBoard()
    for position, color in crop_image.find_pieces(warped):
        checker_board.set_piece(position//8, position%8, color)
    # print(checker_board.board)
    checker_board.print_me()
    move = checker_board.find_moves(Color.BLACK)
    print(move)
    cv2.imshow('xd', warped)
    cv2.waitKey()


if __name__ == '__main__':
    main()

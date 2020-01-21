import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import numpy as np
from screenchess.checkers.checker_board import CheckerBoard
from screenchess.checkers.color import Color
from contextlib import contextmanager
from screenchess.chessboard_recognition import visualization
from screenchess.chessboard_recognition import crop_image, recognize_chessboard, clusterlist
import chess


def main():
    # camera = PiCamera()
    # camera.resolution = (640, 480)
    # camera.framerate = 15
    # rawCapture = PiRGBArray(camera, size=(640, 480))
    # time.sleep(0.4)
    
    # for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # markers = recognize_chessboard.find_markers(frame.array)
    # cv2.imshow('xd', frame.array)
    # key = cv2.waitKey(1) & 0xFF
    img = cv2.imread('images/input/9.jpg')
    # markers = recognize_chessboard.find_markers(frame.array)
    # if markers is None or len(markers) > 2000:
    #     rawCapture.truncate(0)
    #     continue
    # print(len(markers))
    markers = recognize_chessboard.find_markers(img)
    cluster = clusterlist.ClusterList(lambda x, y: np.linalg.norm(x - y) < 60,
                                      lambda x, y: ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2))
    for point in markers:
        cluster.append(point[0])
    cluster.trim(5)

    # if len(cluster.data) != 4:
    #     rawCapture.truncate(0)
    #     continue

    # warped = recognize_chessboard.top_down_transform(frame.array, np.array(cluster.data))
    warped = recognize_chessboard.top_down_transform(img, np.array(cluster.data))
    checker_board = CheckerBoard()
    for position, color in crop_image.find_pieces(warped):
        checker_board.set_piece(position//8, position % 8, color)

    # checker_board.print_me()
    move = checker_board.find_moves(Color.WHITE)
    if move:
        move = move[0], move[1][0]
        print(move)
        arrow = visualization.visualize_move(warped, move)
        cv2.imshow('xd', arrow)
        cv2.waitKey()
    else:
        cv2.imshow('xd', warped)
        cv2.waitKey()
    # key = cv2.waitKey(1) & 0xFF

    # rawCapture.truncate(0)
    # if key == ord('q'):
    #     break


if __name__ == '__main__':
    main()

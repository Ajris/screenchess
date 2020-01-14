import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from checkers.checker_board import CheckerBoard
from checkers.color import Color
from contextlib import contextmanager
from chessboard_recognition import crop_image, recognize_chessboard, clusterlist


def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 15
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.4)
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        markers = recognize_chessboard.find_markers(frame.array)
        #cv2.imshow('xd', frame.array)
        #key = cv2.waitKey(1) & 0xFF
        if markers is None or len(markers) > 2000:
            rawCapture.truncate(0)
            continue
        #print(len(markers))
        cluster = clusterlist.ClusterList(lambda x, y: np.linalg.norm(x - y) < 40,
                                          lambda x, y: ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2))
        for point in markers:
            cluster.append(point[0])
        cluster.trim(5)

        if len(cluster.data) != 4:
            rawCapture.truncate(0)
            continue
        
        warped = recognize_chessboard.top_down_transform(frame.array, np.array(cluster.data))
        checker_board = CheckerBoard()
        for position, color in crop_image.find_pieces(warped):
            checker_board.set_piece(position//8, position % 8, color)
        
        checker_board.print_me()
        move = checker_board.find_moves(Color.WHITE)
        print(move)
        
        cv2.imshow('xd', warped)
        key = cv2.waitKey(1) & 0xFF
        
        rawCapture.truncate(0)
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()

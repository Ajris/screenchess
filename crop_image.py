import cv2.cv2 as cv2
import numpy as np

from config import BOARD_DIM, IMAGE_DIRECTORY


def chessboard_squares(img):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    for i in range(BOARD_DIM):
        for j in range(BOARD_DIM):
            yield i, j, img[i * width:(i+1) * width, j * height:(j+1) * height]


def find_pieces(thresh):
    for x, y, square in chessboard_squares(thresh):
        if is_occupied(square):
            _file = f'{x}:{y}.jpg'
            cv2.imwrite(IMAGE_DIRECTORY + _file, square)


def is_occupied(thresh):
    height = int(thresh.shape[0] / np.sqrt(2))
    width = int(thresh.shape[1] / np.sqrt(2))

    start_x = int((thresh.shape[0] - height) / 2)
    end_x = int((thresh.shape[0] + height) / 2)

    start_y = int((thresh.shape[1] - width) / 2)
    end_y = int((thresh.shape[1] + width) / 2)

    aoi = thresh[start_y:end_y, start_x:end_x]

    intersection = np.logical_not(aoi)

    return intersection.any()

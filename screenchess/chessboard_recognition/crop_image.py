import cv2.cv2 as cv2
import numpy as np
from ..checkers.color import Color
from ..config import BOARD_DIM


def detect_edges(img):
    contoured_img = img.copy()
    imgray = cv2.cvtColor(contoured_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)
    contours, _ = cv2.findContours(thresh,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contoured_img, contours, -1, (0, 255, 0), 3)
    return contoured_img, thresh, contours


def chessboard_squares(img):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    for i in range(BOARD_DIM):
        for j in range(BOARD_DIM):
            yield i, j, img[i * width:(i + 1) * width, j * height:(j + 1) * height]


def find_pieces(img):
    for x, y, square in chessboard_squares(img):
        _, thresh, _ = detect_edges(square)
        aoi = get_aoi(square)
        xd = np.array(aoi).mean(axis=(0, 1))
        if is_occupied(thresh):
            position = (7 - x) * 8 + y
            yield position, Color.WHITE if xd.mean() > 120 else Color.BLACK


def get_aoi(img):
    height = img.shape[0] // 2
    width = img.shape[1] // 2

    start_x = (img.shape[0] - height) // 2
    end_x = (img.shape[0] + height) // 2

    start_y = (img.shape[1] - width) // 2
    end_y = (img.shape[1] + width) // 2

    aoi = img[start_y:end_y, start_x:end_x]
    return aoi


def is_occupied(thresh):
    intersection = np.logical_not(get_aoi(thresh))
    return intersection.any()

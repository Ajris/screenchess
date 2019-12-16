import cv2.cv2 as cv2
import numpy as np
import webcolors
import chess

from config import BOARD_DIM, IMAGE_DIRECTORY


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


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def chessboard_squares(img):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    for i in range(BOARD_DIM):
        for j in range(BOARD_DIM):
            yield i, j, img[i * width:(i + 1) * width, j * height:(j + 1) * height]


def chessboard_squares1(img, i, j):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    return img[i * width:(i + 1) * width, j * height:(j + 1) * height]


def find_pieces(img):
    _, thresh, _ = detect_edges(img)
    for x, y, square in chessboard_squares(img):
        aoi = get_aoi(square)
        xd = np.array(aoi).mean(axis=(0, 1))
        if is_occupied(chessboard_squares1(thresh, x, y)):
            position = (7 - x) * 8 + y
            yield position, chess.WHITE if xd.mean() > 120 else chess.BLACK


def get_aoi(img):
    height = int(img.shape[0] / np.sqrt(2))
    width = int(img.shape[1] / np.sqrt(2))

    start_x = int((img.shape[0] - height) / 2)
    end_x = int((img.shape[0] + height) / 2)

    start_y = int((img.shape[1] - width) / 2)
    end_y = int((img.shape[1] + width) / 2)

    return img[start_y:end_y, start_x:end_x]


def is_occupied(thresh):
    intersection = np.logical_not(get_aoi(thresh))
    return intersection.any()

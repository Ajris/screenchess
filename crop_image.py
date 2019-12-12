import cv2.cv2 as cv2
import numpy as np
import webcolors

from config import BOARD_DIM, IMAGE_DIRECTORY

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
            yield i, j, img[i * width:(i+1) * width, j * height:(j+1) * height]

def chessboard_squares1(img, i, j):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    return img[i * width:(i+1) * width, j * height:(j+1) * height]


def find_pieces(img, thresh, c):
    for x, y, square in chessboard_squares(img):

        height = int(square.shape[0] / 2)
        width = int(square.shape[1] / 2)

        start_x = int((square.shape[0] - height) / 2)
        end_x = int((square.shape[0] + height) / 2)

        start_y = int((square.shape[1] - width) / 2)
        end_y = int((square.shape[1] + width) / 2)

        aoi = square[start_y:end_y, start_x:end_x]
        xd = np.array(aoi).mean(axis=(0,1))
        if is_occupied(chessboard_squares1(thresh, x, y)):
            if xd.mean() > 120.0:
                _file = f'{x}:{y}W.jpg'
            else:
                _file = f'{x}:{y}B.jpg'

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

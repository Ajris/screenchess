import cv2.cv2 as cv2
import numpy as np

from config import BOARD_DIM, IMAGE_DIRECTORY


def detect_edges(img, save=False):
    print('xdd')
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)
    bin_thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    close = cv2.morphologyEx(bin_thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, _ = cv2.findContours(close,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cv2.fillPoly(close, contours, [255, 255, 255])
    mask = np.zeros(imgray.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, 255, -1)
    mean = cv2.mean(imgray, mask=mask)
    # if save:
    #     cv2.imshow('xd', )
    #     cv2.waitKey()
    return thresh, mean[0] >= 255 / 2


# TODO
"""
Morphology based binarization
"""
# def find_piece_color(img):
#     blur = cv2.GaussianBlur(img,(5,5),0)
#     _, img_binary = cv2.threshold(blur,130,255,cv2.THRESH_BINARY)
#     img_binary_inverted = cv2.bitwise_not(img_binary)
#     morph_kernel = np.ones((15,15),np.uint8)
#     output = cv2.morphologyEx(img_binary_inverted, cv2.MORPH_CLOSE, morph_kernel)
#     return output


def chessboard_squares(img):
    height = img.shape[0] // BOARD_DIM
    width = img.shape[1] // BOARD_DIM
    for i in range(BOARD_DIM):
        for j in range(BOARD_DIM):
            yield i, j, img[i * width:(i+1) * width, j * height:(j+1) * height]


def get_binary_chessboard(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(5,5),0)
    _, img_binary = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img_binary


def find_pieces(img):
    for x, y, square in chessboard_squares(img):
        thresh, color = detect_edges(square, (x, y) == (3, 6))
        if is_occupied(thresh):
            _file = f'{x}:{y}_{color}.jpg'
            cv2.imwrite(IMAGE_DIRECTORY + _file, thresh)


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

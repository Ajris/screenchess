import cv2.cv2 as cv2
import numpy as np

from config import CHESSBOARD_DIMENSION, IMAGE_DIRECTORY


def get_cropped_images(img, thresh):
    height = int(img.shape[0] / CHESSBOARD_DIMENSION)
    width = int(img.shape[1] / CHESSBOARD_DIMENSION)

    for i in range(CHESSBOARD_DIMENSION):
        for j in range(CHESSBOARD_DIMENSION):
            cropped_img = img[i * width:(i + 1) * width, j * height:(j + 1) * height]
            cropped_threshold = thresh[i * width:(i + 1) * width, j * height:(j + 1) * height]

            chesspiece = check_piece(cropped_threshold)
            if chesspiece:
                filename = f'{i}:{j}.png'
                cv2.imwrite(IMAGE_DIRECTORY + filename, cropped_threshold)


def check_piece(thresh):
    height = int(thresh.shape[0] / np.sqrt(2))
    width = int(thresh.shape[1] / np.sqrt(2))

    start_x = int((thresh.shape[0] - height) / 2)
    end_x = int((thresh.shape[0] + height) / 2)

    start_y = int((thresh.shape[1] - width) / 2)
    end_y = int((thresh.shape[1] + width) / 2)

    aoi = thresh[start_y:end_y, start_x:end_x]

    intersection = np.logical_not(aoi)

    return intersection.any()

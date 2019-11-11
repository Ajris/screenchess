import cv2.cv2 as cv2
from config import CHESSBOARD_DIMENSION, IMAGE_DIRECTORY


def save_cropped_images(img):
    height = int(img.shape[0] / CHESSBOARD_DIMENSION)
    width = int(img.shape[1] / CHESSBOARD_DIMENSION)

    for i in range(CHESSBOARD_DIMENSION):
        for j in range(CHESSBOARD_DIMENSION):
            cropped_img = img[i * width:(i + 1) * width, j * height:(j + 1) * height]
            filename = f'{i}:{j}.png'
            cv2.imwrite(IMAGE_DIRECTORY + filename, cropped_img)

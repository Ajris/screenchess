import cv2
import detect_pieces
import crop_image
import numpy as np


def main():
    img = cv2.imread('images/board1.jpg')
    detected_pieces_image = detect_pieces.detect_edges(img)
    crop_image.save_cropped_images(detected_pieces_image)


if __name__ == '__main__':
    main()

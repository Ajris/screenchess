import cv2
import numpy as np
from matplotlib import pyplot as plt

directory = 'images/'

def saveCroppedImages(img):
    height = int(img.shape[0] / 8)
    width = int(img.shape[1] / 8)

    for i in range(0, 8):
        for j in range(0, 8):
            cropped_img = img[i*width:(i+1)*width, j*height:(j+1)*height]
            imgray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 120, 255, 0)
            contours, hierarchy = cv2.findContours(thresh,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(cropped_img, contours, -1, (0, 255, 0), 3)
            filename = f'{i}:{j}.png'
            cv2.imwrite(directory + filename, cropped_img)


def main():
    img = cv2.imread('images/board.jpg')
    saveCroppedImages(img)

if __name__ == '__main__':
    main()

import numpy as np
import cv2.cv2 as cv2


def draw_hough_lines(img):
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200)
    # for rho, theta in lines[0]:
    #     a, b = np.cos(theta), np.sin(theta)
    #     x0, y0 = a * rho, b * rho
    #     x1, y1 = int(x0 - 1000 * b), int(y0 + 1000 * a)
    #     x2, y2 = int(x0 + 1000 * b), int(y0 - 1000 * a)
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    a, b, c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]),
                 (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
    return img


def approximate_corners(img, dimensions):
    found, corners = cv2.findChessboardCorners(img, dimensions)
    return found


if __name__ == '__main__':
    img = cv2.imread('/home/kshalot/Pictures/untransformed_chessboard.jpg')
    print(approximate_corners(img, (8,8)))
    # lines = draw_hough_lines(img)
    # cv2.imshow('lines', lines)
    # cv2.waitKey()

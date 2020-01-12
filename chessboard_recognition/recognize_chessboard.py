import numpy as np
import cv2.cv2 as cv2
from .clusterlist import ClusterList


def get_board_lines(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    min_length = 120
    max_gap = 70
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=80, minLineLength=min_length, maxLineGap=max_gap)
    for line in lines:
        print(line)
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return lines


def find_markers(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask0 + mask1
    # cv2.imshow('xd', cv2.bitwise_and(img, img, mask=mask))
    # cv2.waitKey()
    points = cv2.findNonZero(mask)
    return points


def order_points(points):
    rect = np.zeros((4, 2), dtype="float32")
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]
    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]
    print(rect)
    return rect


def top_down_transform(img, points):
    rect = order_points(points)
    tl, tr, br, bl = rect
    a_width = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    b_width = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(a_width), int(b_width))

    a_height = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    b_height = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(a_height), int(b_height))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_width - 1],  # [max_width - 1, max_height - 1]
        [0, max_width - 1]  # max_height - 1
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (max_width, max_width))  # (max_width, max_height)
    return warped


if __name__ == '__main__':
    img = cv2.imread('images/input/test3.jpg')
    markers = find_markers(img)
    cluster = ClusterList(lambda x, y: np.linalg.norm(x - y) < 40)
    for point in markers:
        cluster.append(point[0])
    warped = top_down_transform(img, np.array(cluster.data))
    cv2.imshow('xd', warped)
    cv2.waitKey()

import cv2
import detect_pieces
import crop_image


def main():
    img = cv2.imread('images/input/board.jpg')
    detected_pieces_image, threshold, contours = detect_pieces.detect_edges(img)
    crop_image.find_pieces(detected_pieces_image, threshold, contours)


if __name__ == '__main__':
    main()

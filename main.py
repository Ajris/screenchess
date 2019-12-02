import cv2
import detect_pieces
import crop_image


def main():
    img = cv2.imread('images/board1.jpg')
    detected_pieces_image, threshold = detect_pieces.detect_edges(img)
    crop_image.find_pieces(threshold)


if __name__ == '__main__':
    main()

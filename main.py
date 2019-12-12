import cv2.cv2 as cv2
import crop_image


def main():
    img = cv2.imread('images/board1.jpg')
    crop_image.find_pieces(img)
    cv2.imwrite('images/bin2.jpg', crop_image.get_binary_chessboard(img))


if __name__ == '__main__':
    main()

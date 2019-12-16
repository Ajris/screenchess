import cv2
import crop_image
import chess

from board_recognition.main import detect_chessboard


def main():
    detect_chessboard('detect', '../images/input/board6.jpg', '../images/output/output6.jpg')
    img = cv2.imread('../images/output/output6.jpg')
    print(img is None)
    board = chess.Board(None)
    # detected_pieces_image, threshold, contours = detect_pieces.detect_edges(img)
    for position, color in crop_image.find_pieces(img):
        board.set_piece_at(position, chess.Piece(chess.PAWN, color))
    return board.fen()


if __name__ == '__main__':
    print(main())

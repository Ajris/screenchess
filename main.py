import cv2
import crop_image
import chess


def main():
    img = cv2.imread('images/input/board1.jpg')
    board = chess.Board(None)
    # detected_pieces_image, threshold, contours = detect_pieces.detect_edges(img)
    for position, color in crop_image.find_pieces(img):
        board.set_piece_at(position, chess.Piece(chess.PAWN, color))
    print(board.fen())


if __name__ == '__main__':
    main()

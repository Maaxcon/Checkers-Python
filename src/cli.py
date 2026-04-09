from __future__ import annotations

from .board import create_initial_board
from .types import Board, Piece


def piece_to_char(piece: Piece | None) -> str:
    if piece is None:
        return "."
    if piece.player == "light":
        return "W" if piece.is_king else "w"
    return "B" if piece.is_king else "b"


def print_board(board: Board) -> None:
    print("   " + " ".join(str(col) for col in range(8)))
    for row_index, row in enumerate(board):
        row_str = " ".join(piece_to_char(cell) for cell in row)
        print(f"{row_index}  {row_str}")


if __name__ == "__main__":
    board = create_initial_board()
    print_board(board)

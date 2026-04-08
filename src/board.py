from __future__ import annotations

from typing import Optional

from .constants import BOARD, PLAYERS
from .types import Board, Piece, Player


def create_piece(player: Player, is_king: bool = False) -> Piece:
    return Piece(player=player, is_king=is_king)


def create_initial_board() -> Board:
    grid: Board = []
    for _row in range(BOARD.ROWS):
        grid_row: list[Optional[Piece]] = []
        for _col in range(BOARD.COLS):
            grid_row.append(None)
        grid.append(grid_row)

    for row in range(BOARD.ROWS):
        for col in range(BOARD.COLS):
            if (row + col) % 2 != 0:
                if row < BOARD.PIECE_ROWS:
                    grid[row][col] = create_piece(PLAYERS.DARK)
                elif row >= BOARD.ROWS - BOARD.PIECE_ROWS:
                    grid[row][col] = create_piece(PLAYERS.LIGHT)

    return grid


def clone_board(board: Board) -> Board:
    return [
        [Piece(player=piece.player, is_king=piece.is_king) if piece else None for piece in row]
        for row in board
    ]


def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < BOARD.ROWS and 0 <= col < BOARD.COLS


def get_piece(board: Board, row: int, col: int) -> Optional[Piece]:
    if not is_valid_position(row, col):
        return None
    return board[row][col]

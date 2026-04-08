from __future__ import annotations

from typing import Optional

from .board import get_piece, is_valid_position
from .constants import DIRECTIONS, GAME_SETTINGS, PLAYERS
from .types import Board, CaptureMove, Move, MoveType, Piece


def is_opponent(piece: Piece, other: Optional[Piece]) -> bool:
    return other is not None and piece.player != other.player


def get_move_directions(piece: Piece) -> list[int]:
    if piece.is_king:
        return [DIRECTIONS.UP, DIRECTIONS.DOWN]
    return [DIRECTIONS.UP] if piece.player == PLAYERS.LIGHT else [DIRECTIONS.DOWN]


def get_moves_for_piece(board: Board, row: int, col: int) -> list[MoveType]:
    piece = get_piece(board, row, col)
    if piece is None:
        return []
    if piece.is_king:
        return get_king_moves(board, row, col, piece)
    return get_normal_piece_moves(board, row, col, piece)


def get_normal_piece_moves(board: Board, row: int, col: int, piece: Piece) -> list[MoveType]:
    moves: list[MoveType] = []
    directions_y = get_move_directions(piece)
    directions_x = [-1, 1]

    for direction_y in directions_y:
        for direction_x in directions_x:
            new_row = row + direction_y
            new_col = col + direction_x

            if is_valid_position(new_row, new_col):
                target_piece = get_piece(board, new_row, new_col)
                if target_piece is None:
                    moves.append(Move(row=new_row, col=new_col))

    capture_directions = [
        {"row_offset": -1, "col_offset": -1},
        {"row_offset": -1, "col_offset": 1},
        {"row_offset": 1, "col_offset": -1},
        {"row_offset": 1, "col_offset": 1},
    ]

    for direction in capture_directions:
        jump_row = row + direction["row_offset"] * GAME_SETTINGS.JUMP_DISTANCE
        jump_col = col + direction["col_offset"] * GAME_SETTINGS.JUMP_DISTANCE
        middle_row = row + direction["row_offset"]
        middle_col = col + direction["col_offset"]

        if not is_valid_position(jump_row, jump_col):
            continue

        middle_piece = get_piece(board, middle_row, middle_col)
        target_piece = get_piece(board, jump_row, jump_col)

        if target_piece is None and is_opponent(piece, middle_piece):
            moves.append(
                CaptureMove(
                    row=jump_row,
                    col=jump_col,
                    captured_row=middle_row,
                    captured_col=middle_col,
                )
            )

    return moves


def get_king_moves(board: Board, row: int, col: int, piece: Piece) -> list[MoveType]:
    moves: list[MoveType] = []
    directions = [
        {"row_offset": -1, "col_offset": -1},
        {"row_offset": -1, "col_offset": 1},
        {"row_offset": 1, "col_offset": -1},
        {"row_offset": 1, "col_offset": 1},
    ]

    for direction in directions:
        current_row = row + direction["row_offset"]
        current_col = col + direction["col_offset"]
        found_enemy: Optional[tuple[int, int]] = None

        while is_valid_position(current_row, current_col):
            target_piece = get_piece(board, current_row, current_col)

            if found_enemy is None:
                if target_piece is None:
                    moves.append(Move(row=current_row, col=current_col))
                elif is_opponent(piece, target_piece):
                    found_enemy = (current_row, current_col)
                else:
                    break
            else:
                if target_piece is None:
                    moves.append(
                        CaptureMove(
                            row=current_row,
                            col=current_col,
                            captured_row=found_enemy[0],
                            captured_col=found_enemy[1],
                        )
                    )
                else:
                    break

            current_row += direction["row_offset"]
            current_col += direction["col_offset"]

    return moves

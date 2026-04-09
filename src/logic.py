from __future__ import annotations

from typing import Optional

from .board import clone_board, get_piece, is_valid_position
from .constants import BOARD, PLAYERS
from .moves import get_moves_for_piece
from .types import Board, CaptureMove, MoveType, Piece, Player


def apply_move(board: Board, move: MoveType) -> Board:
    if not is_valid_position(move.from_row, move.from_col):
        raise ValueError("Source position is out of board bounds")
    if not is_valid_position(move.row, move.col):
        raise ValueError("Target position is out of board bounds")

    legal_moves = get_legal_moves_for_piece(board, move.from_row, move.from_col)
    if move not in legal_moves:
        raise ValueError("Move is not legal for the selected piece")

    new_board = clone_board(board)

    piece = new_board[move.from_row][move.from_col]
    if piece is None:
        raise ValueError("No piece at source position")
    if new_board[move.row][move.col] is not None:
        raise ValueError("Target square is not empty")

    new_board[move.from_row][move.from_col] = None

    if move.type == "capture":
        if not is_valid_position(move.captured_row, move.captured_col):
            raise ValueError("Captured position is out of board bounds")

        captured_piece = new_board[move.captured_row][move.captured_col]
        if captured_piece is None:
            raise ValueError("No piece to capture at captured position")
        if captured_piece.player == piece.player:
            raise ValueError("Cannot capture your own piece")

        new_board[move.captured_row][move.captured_col] = None

    reached_promotion_row = (
        (piece.player == PLAYERS.LIGHT and move.row == 0)
        or (piece.player == PLAYERS.DARK and move.row == BOARD.ROWS - 1)
    )
    is_king = piece.is_king or reached_promotion_row

    new_board[move.row][move.col] = Piece(player=piece.player, is_king=is_king)
    return new_board


def get_winner(board: Board, turn: Player) -> Optional[Player]:
    if not _player_has_pieces(board, PLAYERS.LIGHT):
        return PLAYERS.DARK
    if not _player_has_pieces(board, PLAYERS.DARK):
        return PLAYERS.LIGHT

    if not get_legal_moves_for_player(board, turn):
        return get_opponent(turn)

    return None


def get_legal_moves_for_player(board: Board, player: Player) -> list[MoveType]:
    player_moves = _get_player_moves(board, player)
    capture_moves = _filter_capture_moves(player_moves)
    if capture_moves:
        return capture_moves
    return player_moves


def get_legal_moves_for_piece(board: Board, row: int, col: int) -> list[MoveType]:
    piece = get_piece(board, row, col)
    if piece is None:
        return []

    piece_moves = get_moves_for_piece(board, row, col)
    if not piece_moves:
        return []

    player_capture_moves = _filter_capture_moves(_get_player_moves(board, piece.player))
    if not player_capture_moves:
        return piece_moves

    return [move for move in piece_moves if move.type == "capture"]


def get_chain_capture_moves(board: Board, row: int, col: int) -> list[CaptureMove]:
    piece = get_piece(board, row, col)
    if piece is None:
        return []

    moves = get_moves_for_piece(board, row, col)
    return [move for move in moves if move.type == "capture"]


def _player_has_pieces(board: Board, player: Player) -> bool:
    for row in board:
        for piece in row:
            if piece is not None and piece.player == player:
                return True
    return False


def _get_player_moves(board: Board, player: Player) -> list[MoveType]:
    player_moves: list[MoveType] = []
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece is None or piece.player != player:
                continue

            piece_moves = get_moves_for_piece(board, row_index, col_index)
            player_moves.extend(piece_moves)

    return player_moves


def _filter_capture_moves(moves: list[MoveType]) -> list[MoveType]:
    return [move for move in moves if move.type == "capture"]


def get_opponent(player: Player) -> Player:
    if player == PLAYERS.LIGHT:
        return PLAYERS.DARK
    return PLAYERS.LIGHT

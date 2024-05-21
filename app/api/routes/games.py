import random
from typing import Literal
import uuid

from fastapi import APIRouter, Depends, status

from app.cache import GameCache
from app.models import Game, GameMove, GameStatus, Move

router = APIRouter()
game_cache = GameCache()


@router.post("", summary="Create a new game", status_code=status.HTTP_201_CREATED)
async def create_game(game: Game = Depends(game_cache.new_game)) -> Game:
    """
    Create a new game of Noughts & Crosses
    """
    return game


@router.get(
    "/{game_id}",
    summary="Retrieve a game",
    responses={404: {"description": "Game not found"}},
)
async def get_game(game: Game = Depends(game_cache.find_game)) -> Game:
    """
    Retrieve an existing game by ID
    """
    return game


@router.get("", summary="List all games")
async def list_games(order: Literal["asc", "desc"] = "asc") -> list[Game]:
    """
    List all the existing games, sorted by createdAt
    """
    all_games = game_cache.list_games()
    all_games.sort(
        key=lambda game: game.created_at,
        reverse=True if order == "desc" else False,
    )
    return all_games


@router.patch(
    "/{game_id}",
    summary="Update a game",
    responses={404: {"description": "Game not found"}},
)
async def update_game(game_id: uuid.UUID, user_move: Move) -> Game:
    """
    Update an existing game by making a game move. A game move
    consists of co-ordinates (x,y) that represent a space on the
    game board. The computer will automatically make a move after
    the players move is completed
    """
    retrieved_game = game_cache.find_game(game_id)

    retrieved_game.check_game_in_progress()
    retrieved_game.capture_move(move=user_move, player="X")

    # check if user won
    winner = retrieved_game.check_winner()
    if winner:
        retrieved_game.status = GameStatus.COMPLETED_USER_WINNER
        return retrieved_game

    # computer move
    available_moves = retrieved_game.get_available_moves()
    if not available_moves:
        retrieved_game.status = GameStatus.COMPLETED_TIE
        return retrieved_game

    retrieved_game.capture_move(move=random.choice(available_moves), player="O")

    # check if computer won
    winner = retrieved_game.check_winner()
    if winner:
        retrieved_game.status = GameStatus.COMPLETED_COMPUTER_WINNER

    return retrieved_game


@router.get("/{game_id}/moves", summary="List all game moves")
async def get_game_moves(
    game: Game = Depends(game_cache.find_game),
) -> dict[str, GameMove]:
    """
    List all the game moves for an existing game by ID
    """
    return game.moves


@router.patch("/{game_id}/forfeit", summary="Forfeit a game")
async def forfeit_game(game: Game = Depends(game_cache.find_game)) -> Game:
    game.check_game_in_progress()
    game.status = GameStatus.FORFEITED

    return game

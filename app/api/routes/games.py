import random

from fastapi import APIRouter, Depends, status

from app.cache import GameCache
from app.models import Game, GameMove, GameStatus

router = APIRouter()
game_cache = GameCache()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_game(game: Game = Depends(game_cache.new_game)) -> Game:
    return game


@router.get("/{game_id}")
async def get_game(game: Game = Depends(game_cache.find_game)) -> Game:
    return game


@router.get("")
async def list_games() -> list[Game]:
    all_games = game_cache.list_games()
    all_games.sort(key=lambda game: game.created_at)
    return all_games


@router.patch("/{game_id}")
async def update_game(game_id: str, game_move: GameMove) -> Game:
    retrieved_game = game_cache.find_game(game_id)

    retrieved_game.check_game_in_progress()
    retrieved_game.capture_move(move=game_move, player="X")

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

    retrieved_game.capture_move(move=random.choice(available_moves), player="Y")

    # check if computer won
    winner = retrieved_game.check_winner()
    if winner:
        retrieved_game.status = GameStatus.COMPLETED_COMPUTER_WINNER

    return retrieved_game

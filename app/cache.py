import uuid

from fastapi import HTTPException

from app.models import Game


# this would ideally be a real db :)
class GameCache:
    def __init__(self) -> None:
        self._games: dict[str, Game] = {}

    def new_game(self) -> Game:
        game = Game(id=str(uuid.uuid4()))
        self._games[game.id] = game

        return game

    def find_game(self, game_id: str) -> Game:
        game = self._games.get(game_id, None)
        if not game:
            raise HTTPException(
                status_code=404,
                detail="No game found for the provided ID",
            )

        return game

    def list_games(self) -> list[Game]:
        return [game for game in self._games.values()]

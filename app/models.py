import datetime
from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, Field
import uuid


class GameMove(BaseModel):
    x: int = Field(ge=0, lt=3, description="Position on the x-axis of the game board")
    y: int = Field(ge=0, lt=3, description="Position on the y-axis of the game board")


class GameStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED_USER_WINNER = "Completed - You Won!"
    COMPLETED_COMPUTER_WINNER = "Completed - Computer Won!"
    COMPLETED_TIE = "Completed - It's a Tie!"
    FORFEITED = "Forfeited"


class Game(BaseModel):
    id: str = Field(default_factory=uuid.uuid4())
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now())
    status: GameStatus = GameStatus.NOT_STARTED
    user_player: str = "X"
    game_board: list[list[str]] = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    moves: dict[str, GameMove] = {}

    def capture_move(self, move: GameMove, player: str) -> None:
        if self.status == GameStatus.NOT_STARTED:
            self.status = GameStatus.IN_PROGRESS

        if self.game_board[move.x][move.y] != ".":
            raise HTTPException(
                status_code=400,
                detail="Unable to make a move at the requested location",
            )

        self.game_board[move.x][move.y] = player
        self.moves[f"Player {player}, move {len(self.moves) // 2}"] = move

    def check_game_in_progress(self) -> None:
        if self.status not in [GameStatus.NOT_STARTED, GameStatus.IN_PROGRESS]:
            raise HTTPException(
                status_code=400,
                detail="The game found for the provided ID has already been completed",
            )

    def get_available_moves(self) -> list[GameMove]:
        available_moves = []
        for row_idx, row in enumerate(self.game_board):
            for col_idx, _ in enumerate(row):
                if self.game_board[row_idx][col_idx] == ".":
                    available_moves.append(GameMove(x=row_idx, y=col_idx))

        return available_moves

    def check_winner(self) -> str | None:
        winning_patterns = [
            {(0, 0), (0, 1), (0, 2)},
            {(1, 0), (1, 1), (1, 2)},
            {(2, 0), (2, 1), (2, 2)},
            {(0, 0), (1, 0), (2, 0)},
            {(0, 1), (1, 1), (2, 1)},
            {(0, 2), (1, 2), (2, 2)},
            {(0, 0), (1, 1), (2, 2)},
            {(0, 2), (1, 1), (2, 0)},
        ]

        for pattern in winning_patterns:
            symbols = {self.game_board[i][j] for i, j in pattern}
            if len(symbols) == 1 and "." not in symbols:
                return symbols.pop()

        return None

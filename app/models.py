import datetime
from enum import Enum
from typing import Literal, TypeAlias

from fastapi import HTTPException
from pydantic import BaseModel, Field
import uuid

_PLAYER: TypeAlias = Literal["X", "O"]


class Move(BaseModel):
    x: int = Field(ge=0, le=2, description="Position on the x-axis of the game board")
    y: int = Field(ge=0, le=2, description="Position on the y-axis of the game board")


class GameMove(Move):
    player: _PLAYER = Field(description="The player that made the move")


class GameStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED_USER_WINNER = "Completed - You Won!"
    COMPLETED_COMPUTER_WINNER = "Completed - Computer Won!"
    COMPLETED_TIE = "Completed - It's a Tie!"


class Game(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="The ID of the game")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="The date and time when the game was created",
        alias="createdAt",
    )
    status: GameStatus = Field(
        default=GameStatus.NOT_STARTED,
        description="The status of the game",
    )
    user_symbol: str = Field(
        default="X",
        description="The symbol that represents the user on the game board",
        alias="userSymbol",
    )
    computer_symbol: str = Field(
        default="O",
        description="The symbol that represents the computer on the game board",
        alias="computerSymbol",
    )
    game_board: list[list[str]] = Field(
        default=[[".", ".", "."], [".", ".", "."], [".", ".", "."]],
        description="The current state of the game board",
        alias="gameBoard",
    )
    moves: dict[str, GameMove] = Field(
        default_factory=dict,
        description="The list of all the moves performed by both players in the game",
    )

    def capture_move(self, move: Move, player: _PLAYER) -> None:
        if self.status == GameStatus.NOT_STARTED:
            self.status = GameStatus.IN_PROGRESS

        if self.game_board[move.x][move.y] != ".":
            raise HTTPException(
                status_code=400,
                detail="Unable to make a move at the requested location",
            )

        self.game_board[move.x][move.y] = player
        self.moves[f"Move #{len(self.moves) + 1}"] = GameMove(
            player=player,
            **move.dict(),
        )

    def check_game_in_progress(self) -> None:
        if self.status not in [GameStatus.NOT_STARTED, GameStatus.IN_PROGRESS]:
            raise HTTPException(
                status_code=400,
                detail="The game found for the provided ID has already been completed",
            )

    def get_available_moves(self) -> list[Move]:
        available_moves = []
        for row_idx, row in enumerate(self.game_board):
            for col_idx, _ in enumerate(row):
                if self.game_board[row_idx][col_idx] == ".":
                    available_moves.append(Move(x=row_idx, y=col_idx))

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

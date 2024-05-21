from fastapi import FastAPI

from app.api.main import router

app = FastAPI(
    title="Noughts & Crosses",
    description="Welcome to the thrilling game of Noughts & Crosses (otherwise known as tic-tac-toe)! To start playing, make a POST request to `/games`",
)
app.include_router(router)

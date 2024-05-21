import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

_NOT_FOUND = "ccd1f2b6-7933-492a-b02a-827165c0850d"
_GAME_ID = "1f8ad657-3d07-481b-b881-724d72ea00de"


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_create_game(client: TestClient):
    response = client.post("/games")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()


def test_get_game_not_found_throws_404(client: TestClient):
    response = client.get(f"/games/{_NOT_FOUND}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_game(client: TestClient):
    new_game_response = client.post("/games")
    new_game_id = new_game_response.json()["id"]

    response = client.get(f"/games/{new_game_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == new_game_response.json()

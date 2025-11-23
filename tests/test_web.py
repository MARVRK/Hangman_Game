import random

from fsm import GameManager
from .test_fsm import create_game_helper
from fastapi.testclient import TestClient
from web import app

client = TestClient(app)

def test_get_player():
    # Given
    response = client.get(url="/app/v1/get_player", params={"player_id": 1})
    # When
    player = app.state.repo_player.get_player(1)
    # Then
    assert response.status_code == 200
    assert player is not None
    assert player.id == 1
    assert player.player_name == "Test_Player"

def test_get_statistics():
    # Given
    response = client.get(url="/app/v1/get_statistics", params={"player_id": 1})
    # When
    player_data = app.state.repo_player.get_player_stats(1)
    # Then
    assert response.status_code == 200
    assert player_data == [('some_id', 1, 'iphone', '______', 'apple', 'HARD', 0, 'LOST')]

def test_create_game():
    # Given
    response = client.post(url="/app/v1/create_game", json={"player_id":1, "difficulty": "easy"})
    game: GameManager = create_game_helper()
    # When
    random.seed(1)
    game.start_game()
    app.state.repo_game.save_fsm(game)
    # Then
    assert response.status_code == 200
    assert {"game_id": 1,
            "game_hint": "rust"}



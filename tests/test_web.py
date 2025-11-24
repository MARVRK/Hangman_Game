import random
from fsm import GameManager, Player
from repo import MockPlayer, MockGame
from .test_fsm import create_game_helper
from fastapi.testclient import TestClient
from web import create_app,app_production

test_player_mock = MockPlayer(store={1: Player(id=1, player_name="Test_Player")})
test_game_mock = MockGame()
app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
client = TestClient(app_production)

def test_get_player():
    # Given
    response = client.get(url="/app/v1/get_player", params={"player_id": 1})
    # When
    player = app_test.state.repo_player.get_player(1)
    # Then
    assert response.status_code == 200
    assert player is not None
    assert player.id == 1
    assert player.player_name == "Test_Player"

def test_get_statistics():
    # Given
    response = client.get(url="/app/v1/get_statistics", params={"player_id": 1})
    # When
    player_data = app_test.state.repo_player.get_player_stats(1)
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
    app_test.state.repo_game.save_fsm(game)
    # Then
    assert response.status_code == 200
    assert {"game_id": 1,
            "game_hint": "rust"}



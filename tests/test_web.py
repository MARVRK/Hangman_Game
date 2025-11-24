
from fsm import GameManager, Player, GameState, Difficulty
from repo import MockPlayer, MockGame
from fastapi.testclient import TestClient
from web import create_app


def test_get_player():
    # Given
    test_player_mock = MockPlayer(store={1: Player(id=1, player_name="Test_Player")})
    test_game_mock = MockGame(None)
    app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
    client = TestClient(app_test)
    # When
    response = client.get(url="/app/v1/get_player", params={"player_id": 1})
    # Then
    assert response.status_code == 200
    assert response.json() == {"name": "Test_Player"}

def test_get_statistics():
    # Given
    test_player_mock = MockPlayer(store={1: Player(id=1, player_name="Test_Player")})
    test_game_mock = MockGame(None)
    app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
    client = TestClient(app_test)
    # When
    response = client.get(url="/app/v1/get_statistics", params={"player_id": 1})
    # Then
    assert response.status_code == 200
    assert response.json() == {"total_games": 1,
                              "games_lost": 1,
                              "game_won": 0,
                              "games_not_finished": 0}

def test_create_game():
    # Given
    test_player_mock = MockPlayer(None)
    new_game = GameManager(state=GameState.IDLE, level=Difficulty.EASY,player_id=1,output=[], id='test_uuid')
    test_game_mock = MockGame(store={"test_uuid":new_game})
    app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
    client = TestClient(app_test)
    # When
    response = client.post(url="/app/v1/create_game", json={"player_id": 1, "difficulty": "easy"})
    # Then
    assert response.status_code == 200
    assert response.json() == {"game_id": "test_uuid",
                               "game_hint": "rust"}

def test_continue_game():
    # Given
    test_player_mock = MockPlayer(None)
    new_game = GameManager(state=GameState.PLAYING,
                           level=Difficulty.EASY,
                           player_id=1,
                           output=["_"] * len("blazing"),
                           id='test_uuid',
                           selected_word="blazing",
                           tries_left=5)
    test_game_mock = MockGame(store={"test_uuid":new_game})
    app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
    client = TestClient(app_test)
    # When
    response = client.post(url="/app/v1/continue_game", json={"game_id": "test_uuid", "word": "b"})
    # Then
    assert response.status_code == 200
    assert response.json() == [['b', '_', '_', '_', '_', '_', '_'], 'Amount of guess words left: 5']

def test_create_player():
    # Given
    test_player_mock = MockPlayer(Player(id=1, player_name="test_name"))
    test_game_mock = MockGame(None)
    app_test = create_app(repo_game=test_game_mock, repo_player=test_player_mock)
    client = TestClient(app_test)
    # Then
    response = client.post(url="/app/v1/create_player", json={"name": "test_name"})
    # Then
    assert response.status_code == 200
    assert response.json() == [f"message: player with name test_name saved to DB with id 1"]
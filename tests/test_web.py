from fastapi.testclient import TestClient

from fsm import Player
from repo import MockPlayer, GameService, PlayerService
from web import app

client = TestClient(app)

test_repo = MockPlayer(store={1: Player(player_name="Test_Player", id=1)})
test_service = PlayerService(repo=test_repo)

def test_get_player():
    # Given
    response = client.get(url="/app/v1/get_player", params={"player_id": 1})
    # When
    player = test_service.get_player(1)
    # Then
    assert response.status_code == 200
    assert player is not None
    assert player.id == 1
    assert player.player_name == "Test_Player"


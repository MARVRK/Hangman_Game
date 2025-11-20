# implement logic on Fastapi
# prepare and suggest some api's (get, post, like start game and continiue)
import uvicorn
from fastapi import FastAPI

from fsm import GameManager, Difficulty, GameState
from models import PlayerNameModel
from repo import PlayerRepository, GameRepository

app = FastAPI()
player = PlayerRepository()
game = GameRepository()


@app.get("/app/v1/get_player")
def get_player(player_id: int):
    result = player.get_player(player_id)
    if result:
        return {'name': f"{result.player_name}"}
    return f"Player with id {player_id} not found"

@app.get("/app/v1/get_statistics")
def get_statistics(player_id: int):
    query = player_id.get_stats(player_id)
    if query:
        return query
    return {f"No games found with id : {player_id}"}


@app.post("/app/v1/create_game")
def create_game(player_id: int, game_difficulty: str):
    new_game = GameManager(player_id=player_id,
                           level=Difficulty.from_string(game_difficulty.lower()),
                           state=GameState.IDLE,
                           output=[])
    new_game.start_game()
    game.save_fsm(new_game)
    return {"game_id": new_game.id,
            "game_hint": new_game.hint}


@app.post("/app/v1/continue_game")
def continue_game(game_id: str, word: str):
    upload_game = game.get_fsm(game_id)
    result = upload_game.guess_word(word)
    game.save_fsm(upload_game)
    return result


@app.post("/app/v1/create_player")
def create_player(player_name: PlayerNameModel):
    try:
        player.save_player(player_name.name)
        return {f"message: player with name {player_name.name} saved to DB"}
    except Exception as e:
        raise e



if __name__ == "__main__":
    uvicorn.run("core:app")

# GET app/v1/get_statistics
# body :{player: id}
#   if player:
#     return {games_played: int, games_won: int, games_lost: int }
#   return {data: "player not found"}

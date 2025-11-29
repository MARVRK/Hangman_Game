
import uvicorn
from fastapi import FastAPI, APIRouter

from fsm import GameManager, Difficulty, GameState, Player
from schemas import PlayerNameModel, CreateGameModel, ContinueGameModel
from repo import PlayerRepository, GameRepository

production_repo_player = PlayerRepository()
production_repo_fsm = GameRepository()


def create_router(app: FastAPI) -> APIRouter:
    router = APIRouter()

    @router.get("/app/v1/get_player/")
    def get_player(player_id: int):
        result = app.state.repo_player.get_player(player_id)
        if result:
            return {'name': f"{result.player_name}"}
        return f"Player with id {player_id} not found"


    @router.get("/app/v1/get_statistics")
    def get_statistics(player_id: int):
        games_won = 0
        games_lost = 0
        games_not_finished = 0
        query = app.state.repo_player.get_player_stats(player_id)
        if query:
            for data in query:
                if data[-1] == "WON":
                    games_won += 1
                elif data[-1] == "LOST":
                    games_lost += 1
                elif data[-1] == "PLAYING":
                    games_not_finished += 1
            return {"total_games": len(query),
                    "games_lost": games_lost,
                    "game_won": games_won,
                    "games_not_finished": games_not_finished}

        return {f"No games found with player_id : {player_id}"}


    @router.post("/app/v1/create_game")
    def create_game(data: CreateGameModel):
        new_game = GameManager(player_id=data.player_id,
                               level=Difficulty.from_string(data.difficulty.lower()),
                               state=GameState.IDLE,
                               output=[])
        new_game.start_game()
        app.state.repo_game.save_fsm(new_game)
        return {"game_id": new_game.id,
                "game_hint": new_game.hint}


    @router.post("/app/v1/continue_game")
    def continue_game(data: ContinueGameModel):
        upload_game = app.state.repo_game.get_fsm(data.game_id)
        result = upload_game.guess_word(data.word)
        app.state.repo_game.save_fsm(upload_game)
        return result


    @router.post("/app/v1/create_player")
    def create_player(player_name: PlayerNameModel):
         player = app.state.repo_player.save_player(player_name.name)
         if player:
            return {f"message: player with name {player.player_name} saved to DB with id {player.id}"}
         return {"message": "player already exists"}

    return router

def create_app(repo_game: GameRepository,
               repo_player: PlayerRepository) -> FastAPI:
    application = FastAPI()
    application.state.repo_game = repo_game
    application.state.repo_player = repo_player
    router = create_router(application)
    application.include_router(router)

    return application

app = create_app(repo_player=production_repo_player,
                            repo_game=production_repo_fsm)

if __name__ == "__main__":
    uvicorn.run("web:app_production")
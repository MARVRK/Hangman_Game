from pydantic import BaseModel

class PlayerNameModel(BaseModel):
    name: str

class CreateGameModel(BaseModel):
    player_id: int
    difficulty: str

class ContinueGameModel(BaseModel):
    player_id: int
    game_id: int
    word: str

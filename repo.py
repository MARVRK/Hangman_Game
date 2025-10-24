import sqlite3
import uuid
from abc import ABC, abstractmethod
from fsm import GameManager
from repoimpl import DataBase
from fsm import Player

db = DataBase()

class FSMAbstraction(ABC):
    @abstractmethod
    def get_fsm(self, fsm_id: uuid.UUID):
        pass

    @abstractmethod
    def save_fsm(self, game: GameManager):
        pass


class PlayerAbstraction(ABC):
    @abstractmethod
    def get_player(self, player_id: GameManager)->Player:
        pass

    @abstractmethod
    def save_player(self, player_name: str )-> Player:
        pass


class GameRepository(FSMAbstraction):
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db")

    def get_fsm(self, fsm_id: uuid.UUID):
        request = db.get_game(game_id=fsm_id)
        if request:
            return {"game found": f"{request}"}
        return {"message": "no game found"}

    def save_fsm(self, fsm_entity: GameManager):
        try:
            db.store_game(data=fsm_entity)
            return {"message": f"{fsm_entity} successfully saved"}
        except Exception as e:
            raise e


class PlayerRepository(PlayerAbstraction):
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db")

    def get_player(self, player_id: int):
        return db.get_name(player_id)

    def save_player(self, player_name: str):
        return db.store_name(player_name)

import sqlite3
from abc import ABC, abstractmethod
from typing import Union, List

from fsm import GameManager
from repoimpl import DataBase
from fsm import Player

db = DataBase()


class FSMAbstraction(ABC):
    @abstractmethod
    def get_fsm(self, fsm_id: str) -> GameManager:
        pass

    @abstractmethod
    def save_fsm(self, game: GameManager):
        pass


class PlayerAbstraction(ABC):
    @abstractmethod
    def get_player(self, player_id: int) -> Player:
        pass

    def get_payer_stats(self, player_id: int) -> List[tuple]:
        pass

    @abstractmethod
    def save_player(self, player_name: str) -> Player:
        pass


class GameRepository(FSMAbstraction):
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db", check_same_thread=False)

    def get_fsm(self, fsm_id: str) -> GameManager:
        return db.get_game(fsm_id)

    def save_fsm(self, game: GameManager):
        db.save_game(game)


class PlayerRepository(PlayerAbstraction):
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db", check_same_thread=False)

    def get_player(self, player_id: int) -> Player:
        return db.get_name(player_id)

    def get_payer_stats(self, player_id: int) -> List[tuple]:
        return db.get_games_by_player(player_id)

    def save_player(self, player_name: str) -> Player:
        return db.save_name(player_name)

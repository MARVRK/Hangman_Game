from abc import ABC, abstractmethod
from fsm import GameManager

class FSMAbstraction(ABC):
    @abstractmethod
    def get_fsm(self, fsm_id):
        pass

    @abstractmethod
    def save_fsm(self, entity: GameManager):
        pass


class PlayerAbstraction(ABC):
    @abstractmethod
    def get_player(self, player_id):
        pass

    @abstractmethod
    def save_player(self, player: GameManager):
        pass


class GameRepository(FSMAbstraction):
    def get_fsm(self, fsm_id):
        # from repoimpl will be function to gain fsm_id
        request = db.filter(fsm_id)
        if request:
            return {"game found": f"{request}"}
        return {"message": "no game found"}

    def save_fsm(self, fsm_entity):
        #from repoimpl will be function to save fsm_entity
        return {"message": f"{fsm_entity} successfully saved"}


class PlayerRepository(PlayerAbstraction):
    def get_player(self, player_id):
        # from repoimpl will be function to gain fsm_id
        request = db.filter(player_id)
        if request:
            return {"player found": f"{request}"}
        return {"message": "no player found"}

    def save_player(self, player_entity):
        # from repoimpl will be function to save fsm_entity
        return {"message": f"{player_entity} successfully saved"}

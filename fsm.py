from dataclasses import dataclass
from enum import auto, Enum


@dataclass
class PlayerData:
    player_name: str
    scores: int = 0
    level: int = 0


class GameFSM(Enum):
    IDLE = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()
    EXIT = auto()


@dataclass
class GameManager:
    player: PlayerData
    state: GameFSM

    def start_game(self):
        if self.state == GameFSM.IDLE:
            print("Game in awaiting state")

    def play(self):
        if self.state == GameFSM.PLAYING:
            print("Game Started")
        elif self.state == GameFSM.WON:
            self.player.scores += 1
        elif self.state == GameFSM.LOST:
            self.player.scores -= 1

    def end_game(self):
        if self.state == GameFSM.EXIT:
            print("Game Finished")

    def results(self):
        if self.player.scores >= 5:
            self.player.level = 1
        if self.player.scores >= 8:
            self.player.level = 2
        if self.player.scores >= 10:
            self.player.level = 3
        return self.player.scores, self.player.level, self.player.player_name


state = GameManager(PlayerData(player_name="John"), state=GameFSM.WON)
state.play()
state.play()
state.play()
state.play()
print(state.player.scores)
print(state.results())

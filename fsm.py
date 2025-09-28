from dataclasses import dataclass
from enum import auto, Enum
import random


@dataclass
class PlayerData:
    player_name: str

    scores: int = 0
    level: int = 0
    selected_word: str = ""
    hint: str = ""
    tries_left: int = 0


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
    counter = 0
    string_storage = ""
    amount_to_guess = {"easy": 5, "medium": 3, "hard": 2}
    words_to_guess = {"easy": {"blazing": "rust", "superman": "famous comics hero"},
                      "medium": {"digital": "signal is analog or ....", "iqos": "smoke"},
                      "hard": {"iphone": "apple", "python": "so slow"}}
    menus_tab = "1.Start_Game \n2.Start Random Game with Random Difficulty \n3.End_Game"

    def start_game(self):

        if self.state == GameFSM.IDLE:
            print("Launching game in playing state")
            print("Welcome to the hangman game!\ntype :help")

            difficulty = random.choice(list(self.amount_to_guess.keys()))
            level = self.words_to_guess.get(difficulty)

            self.player.tries_left = self.amount_to_guess[difficulty]
            self.player.selected_word = random.choice(list(level.keys()))
            self.player.hint = level[self.player.selected_word]

            self.state = GameFSM.PLAYING

    def guess_word(self, word: str):
        if self.state == GameFSM.PLAYING:
            if word in self.player.selected_word:
                print(f"Correct letter: {word}")
                print(f"Amount of guess words left: {self.player.tries_left - self.counter}")
            else:
                self.counter +=1
                print(f"Incorrect letter: {word}")
                print(f"Wrong, Amount of guess words left: {self.player.tries_left - self.counter}")

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


state = GameManager(PlayerData(player_name="John"), state=GameFSM.IDLE)
state.start_game()
state.guess_word("blazing")
# state.play()
# state.play()
# state.play()
# state.play()
# print(state.player.scores)
# print(state.results())

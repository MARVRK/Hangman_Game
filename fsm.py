from ast import literal_eval
from dataclasses import dataclass
from enum import auto, Enum
import random

words_to_guess = {"easy": {"blazing": "rust", "superman": "famous comics hero"},
                  "medium": {"digital": "signal is analog or ....", "iqos": "smoke"},
                  "hard": {"iphone": "apple", "python": "so slow"}}


@dataclass
class PlayerData:
    player_name: str

    scores: int = 0
    level: int = 0
    selected_word: str = ""
    hint: str = ""
    tries_left: int = 0


class GameState(Enum):
    IDLE = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()


class DifficultLevel(Enum):
    EASY = 5
    MEDIUM = 3
    HARD = 2

    # Add decorator static method for "from_sting", its allows to use methode without exemplar
    @classmethod
    def from_string(cls, level: str):
        match level:
            case "easy":
                return cls.EASY
            case "medium":
                return cls.MEDIUM
            case "hard":
                return cls.HARD
            case _:
                raise TypeError("Invalid level, provide 'easy,medium or hard'")

    def to_sting(self):
        match self:
            case self.EASY:
                return "easy"
            case self.MEDIUM:
                return "medium"
            case self.HARD:
                return "hard"


@dataclass
class GameManager:
    player: PlayerData
    state: GameState
    level: DifficultLevel
    counter = 0
    string_storage = ""
    message = []

    def start_game(self):
        if self.state == GameState.IDLE:
            # Initialize level what user typed
            level = words_to_guess.get(self.level.to_sting())

            self.player.tries_left = self.level.value
            self.player.selected_word = random.choice(list(level.keys()))
            self.player.hint = level[self.player.selected_word]
            self.state = GameState.PLAYING

        else:
            raise ValueError("Start Game starts from IDLE")

    # move main logic from main to FSM.py
    # message use one or list messages to rise prints
    def guess_word(self, word: str):
        if self.state == GameState.PLAYING:
            if self.player.tries_left - self.counter -1 != 0:
                if word in self.player.selected_word:
                    message = f"Amount of guess words left: {self.player.tries_left - self.counter}"
                    return message
                else:
                    self.counter += 1
                    message = f"Amount of guess words left: {self.player.tries_left - self.counter}"
                    return message
            else:
                message = "Sorry you lost"
                self.state = GameState.LOST
                return message
        else:
            raise ValueError("Guess word should have state PLAYING")


    def results(self):
        if self.player.scores >= 5:
            self.player.level = 1
        if self.player.scores >= 8:
            self.player.level = 2
        if self.player.scores >= 10:
            self.player.level = 3
        return self.player.scores, self.player.level, self.player.player_name


if __name__ == "__main__":
    print("Launching game in playing state")
    print("Welcome to the hangman game!")
    menus_tab = "Please select event "

    game = GameManager(PlayerData(player_name=input("Please provide name: ").strip()),
                        state=GameState.IDLE,
                        level=DifficultLevel.from_string(
                            input("Please select level easy, medium or hard: ").strip().lower()))
    game.start_game()
    print(f"Game Started, guess word |{game.player.hint}| or type 'exit' to quite ")

while True:

    user_input = input().strip().lower()

    if user_input == "exit" :
        print("shutting down the game...")
        break
    try:
        result = game.guess_word(user_input)
        print(result)
        if game.state == GameState.LOST:
            break
        elif game.state == GameState.WON:
            break


    except KeyboardInterrupt:
        raise "Program Interrupted"
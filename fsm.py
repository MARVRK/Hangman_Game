import uuid
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


class GameState(Enum):
    IDLE = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()


class Difficulty(Enum):
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


@dataclass
class WordsToGuess:
    hint: str
    word: str


WORDS_TO_GUESS = {Difficulty.EASY: [WordsToGuess(word="blazing", hint="rust"),
                                    WordsToGuess(word="superman", hint="famous comics hero")],
                  Difficulty.MEDIUM: [WordsToGuess(word="digital", hint="signal is analog or ...."),
                                      WordsToGuess(word="iqos", hint="smoke")],
                  Difficulty.HARD: [WordsToGuess(word="iphone", hint="apple"),
                                    WordsToGuess(word="python", hint="so slow")]}


@dataclass
class GameManager:
    id = uuid.uuid4()
    player = 1
    state: GameState
    level: Difficulty
    counter = 0
    output = list[str] | None

    def start_game(self):
        if self.state == GameState.IDLE:
            # Initialize level what user typed
            level = WORDS_TO_GUESS.get(self.level)

            self.player.tries_left = self.level.value
            random_word = random.choice(level)
            self.player.selected_word = random_word.word
            self.player.hint = random_word.hint
            self.output = ["_"] * len(self.player.selected_word)
            self.state = GameState.PLAYING
        else:
            raise ValueError("Start Game starts from IDLE")

    def guess_word(self, word: str):
        if self.state != GameState.PLAYING:
            raise ValueError("Guess word should have state PLAYING")

        if word in self.player.selected_word:
            for number, letter in enumerate(self.player.selected_word):
                if letter == word:
                    self.output[number] = word
        else:
            self.counter += 1

        if "_" not in self.output :
            self.state = GameState.WON
            self.player.scores += 1
            return "You won!"

        if self.counter >= self.player.tries_left:
            self.state = GameState.LOST
            if self.player.scores > 0:
                self.player.scores -= 1
            return "Sorry, you lost"

        return f"Amount of guess words left: {self.player.tries_left - self.counter}", self.output

    def results(self):
        if self.player.scores >= 5:
            self.player.level = 1
        if self.player.scores >= 8:
            self.player.level = 2
        if self.player.scores >= 10:
            self.player.level = 3
        return (f"Name:{self.player.player_name} "
                f"Your Score:{self.player.scores} "
                f"Your level:{self.player.level}")




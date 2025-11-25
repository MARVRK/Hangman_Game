import uuid
from dataclasses import dataclass
from enum import auto, Enum
import random



@dataclass
class Player:
    id: int
    player_name: str


class GameState(Enum):
    IDLE = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()


class Difficulty(Enum):
    EASY = 5
    MEDIUM = 3
    HARD = 2

    # A decorator "classmethod" for "from_sting", its allows to use methode without exemplar
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


class GameManager:
    def __init__(self, player_id: int,
                 state: GameState,
                 level: Difficulty,
                 output: list[str],
                 words_to_guess : dict[Difficulty, list[WordsToGuess]] = WORDS_TO_GUESS,
                 hint: str = "",
                 tries_left: int = 0,
                 selected_word: str = "",
                 counter: int = 0,
                 id = None):

        self.id = id if id is not None else uuid.uuid4()
        self.player_id = player_id
        self.state = state
        self.level = level
        self.counter = counter
        self.output = output
        self.selected_word = selected_word
        self.hint = hint
        self.word_to_guess = words_to_guess
        self.tries_left = tries_left

    def start_game(self):
        if self.state == GameState.IDLE:
            # Initialize level what user typed
            level = self.word_to_guess.get(self.level)

            self.tries_left = self.level.value

            random_word = random.choice(level)
            self.selected_word = random_word.word
            self.hint = random_word.hint
            self.output = ["_"] * len(self.selected_word)
            self.state = GameState.PLAYING
        else:
            raise ValueError("Start Game starts from IDLE")

    def guess_word(self, word: str):
        if self.state != GameState.PLAYING:
            raise ValueError("Guess word should have state PLAYING")

        if word in self.selected_word:
            for number, letter in enumerate(self.selected_word):
                if letter == word:
                    self.output[number] = word
        else:
            self.counter += 1
            self.tries_left = self.tries_left - self.counter

        if "_" not in self.output:
            self.state = GameState.WON
            # self.player.scores += 1
            return "You won!"

        if self.counter > self.tries_left:
            self.state = GameState.LOST
            # if self.player.scores > 0:
            #     self.player.scores -= 1
            return "Sorry, you lost"

        return self.output, f"Amount of guess words left: {self.tries_left}"

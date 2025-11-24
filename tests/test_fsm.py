import random
import pytest

from ..fsm import GameManager, GameState, Difficulty, WORDS_TO_GUESS, WordsToGuess


def create_game_helper()-> GameManager:
    return GameManager(player_id=1,
                       state=GameState.IDLE,
                       level=Difficulty.EASY,
                       output=[],
                       id=None)

def test_start_game():
    game : GameManager = create_game_helper()
    # Given:
    random.seed(1)
    level = WORDS_TO_GUESS.get(game.level)
    random_word = random.choice(level)
    # When:
    game.start_game()
    # Then:
    assert game.state == GameState.PLAYING
    assert game.selected_word == random_word.word
    assert game.tries_left == Difficulty.EASY.value
    assert game.hint == random_word.hint
    assert game.output == ["_"] * len(game.selected_word)

    with pytest.raises(ValueError) as err:
        game.start_game()

    assert "IDLE" in str(err.value)

def test_guess_word_valuerr():
    game: GameManager = create_game_helper()
    with pytest.raises(ValueError) as err:
        game.guess_word("m")

    assert "PLAYING" in str(err.value)

def test_guess_word_wrong_word():
    # Given:
    game : GameManager = create_game_helper()
    random.seed(1)
    game.start_game()
    # When:
    game.guess_word("f")
    # Then:
    assert game.counter == 1
    assert game.state == GameState.PLAYING
    assert game.output == ["_"] * len(game.selected_word)
    assert game.guess_word("f") == (game.output, f"Amount of guess words left: {game.tries_left}")

def test_guess_word_correct_word():
    # Given:
    game: GameManager = create_game_helper()
    random.seed(1)
    game.start_game()
    # When:
    game.guess_word("b")
    # Then:
    assert game.tries_left == Difficulty.EASY.value
    assert "b" in game.output

def test_guess_word_win():
    # Given:
    game: GameManager = create_game_helper()
    game.word_to_guess = {Difficulty.EASY: [WordsToGuess(word="b", hint="rust")]}
    game.start_game()
    # When:
    result = game.guess_word("b")
    # Then:
    assert game.state == GameState.WON
    assert game.tries_left == Difficulty.EASY.value
    assert result == "You won!"

def test_guess_word_lose():
    # Given:
    game: GameManager = create_game_helper()
    game.start_game()
    game.tries_left = 0
    # When:
    result = game.guess_word(".")
    # Then:
    assert game.state == GameState.LOST
    assert result == "Sorry, you lost"
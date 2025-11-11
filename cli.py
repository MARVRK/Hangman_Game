import sys
from typing import Optional

from fsm import GameManager, GameState, Difficulty, Player
from repo import PlayerRepository, GameRepository


if __name__ == "__main__":
    player_repo = PlayerRepository()
    game_repo = GameRepository()
    player : Optional[Player] = None
    game : Optional[GameManager] = None


    print("Welcome to the hangman game!")
    init_launch = input("Select Option:\n1.Create Name\n2.Use Name by Id\n").strip()


    if init_launch == "1":
        name = input("please provide your name:").strip()
        player = player_repo.save_player(name)
        if player:
            print(f"Your name {name} has been created with ID {player.id}")
        else:
            raise ValueError(f"Typed Name {name} already Exists")


    elif init_launch == "2":
        repo_id= int(input("please provide you ID:").strip())
        player = player_repo.get_player(repo_id)
        if player:
            print(f"Welcome back {player.player_name}")
        else:
            raise ValueError(f"Not found id {repo_id} in DB")

    game_option = input("Select Option:\n1.Start_New_Game\n2.Find_Game_By_ID\n").strip()

    if game_option == "1":
        game = GameManager(state=GameState.IDLE,
                           player_id=player.id,
                           level=Difficulty.from_string(
                           input("Please select level easy, medium or hard: ").strip().lower()))
        game.start_game()
        print(f"Game Started, guess word |{game.hint}| or type 'exit' to quite ")

    elif game_option == "2":
        old_game_id = input("Please provide Game Id: ").strip()
        game = game_repo.get_fsm(old_game_id)
        if game.state != GameState.PLAYING:
            print("shutting down the game...")
            sys.exit(0)

    while True:
        user_input = input().strip().lower()
        if user_input == "exit":
            print("shutting down the game...")
            game_repo.save_fsm(game)
            break
        try:
            result = game.guess_word(user_input)
            if game.state == GameState.PLAYING:
                print(result)
            if game.state == GameState.LOST:
                print(result)
                game_repo.save_fsm(game)
                break
            if game.state == GameState.WON:
                print(result)
                game_repo.save_fsm(game)
                break

        except KeyboardInterrupt:
            raise "Program Interrupted"

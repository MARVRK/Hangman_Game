from fsm import GameManager, GameState, Difficulty
from repo import PlayerRepository


def game_core() -> GameManager:
    player_repo = PlayerRepository()

    print("Welcome to the hangman game!")
    init_launch = input("Select Option:\n1.Create Name\n2.Use Name by Id\n").strip()

    if init_launch == "1":
        name = input("please provide your name:").strip()
        new_player = player_repo.save_player(name)
        if new_player:
            print(f"Your name {name} has been created with ID {new_player}")
        else:
            raise ValueError(f"Typed Name {name} already Exists")

    elif init_launch == "2":
        repo_id= int(input("please provide you ID:").strip())
        repo_name = player_repo.get_player(repo_id)
        if repo_name is not None:
            print(f"Welcome back {repo_name}")
        else:
            raise ValueError(f"Not found id {repo_id} in DB")

    game = GameManager(state=GameState.IDLE,
                       level=Difficulty.from_string(
                           input("Please select level easy, medium or hard: ").strip().lower()))
    game.start_game()
    print(f"Game Started, guess word |{game.hint}| or type 'exit' to quite ")

    while True:

        user_input = input().strip().lower()
        if user_input == "exit":
            print("shutting down the game...")
            break
        try:
            result = game.guess_word(user_input)
            if game.state == GameState.PLAYING:
                print(result)
            if game.state == GameState.LOST:
                print(result)
                # print(game.results())
                break
            if game.state == GameState.WON:
                print(result)
                # print(game.results())
                break

        except KeyboardInterrupt:
            raise "Program Interrupted"

    return game, game.id

game_core()
from fsm import GameManager, PlayerData, GameState, Difficulty

def game_engine() -> GameManager:
    print("Launching game in playing state")
    print("Welcome to the hangman game!")

    game = GameManager(PlayerData(player_name=input("Please provide name: ").strip()),
                       state=GameState.IDLE,
                       level=Difficulty.from_string(
                           input("Please select level easy, medium or hard: ").strip().lower()))
    game.start_game()
    print(f"Game Started, guess word |{game.player.hint}| or type 'exit' to quite ")

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
                print(game.results())
                break
            if game.state == GameState.WON:
                print(result)
                print(game.results())
                break

        except KeyboardInterrupt:
            raise "Program Interrupted"

    return game
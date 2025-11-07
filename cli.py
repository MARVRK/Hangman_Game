from fsm import GameManager, GameState, Difficulty
from repo import PlayerRepository, GameRepository


if __name__ == "__main__":
    player_repo = PlayerRepository()
    game_repo = GameRepository()
    global player,game, old_game_id

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
        # as old_game_id is global when we create new game , we need to set up it to None
        old_game_id = None
        game.start_game()
        print(f"Game Started, guess word |{game.hint}| or type 'exit' to quite ")

    elif game_option == "2":
        # we are continue playing old game based on uuid
        old_game_id = input("Please provide Game Id: ").strip()
        old_game = game_repo.get_fsm(old_game_id)
        if old_game:
            print(f"Your game uploaded:\n1.Game_ID: {old_game.game_id}"
                  f"\n2.Player_id: {old_game.player_id}"
                  f"\n3.State: {old_game.state}"
                  f"\n4.Difficulty: {old_game.level}"
                  f"\n5.Hint: {old_game.hint}"
                  f"\n6.Guessed_word: {old_game.selected_word}")

            game = GameManager(state=GameState.IDLE,
                               player_id=player.id,
                               level=Difficulty.from_string(
                                   input("Please select level easy, medium or hard: ").strip().lower()))
            game.start_game()
            print(f"Game Started, guess word |{game.hint}| or type 'exit' to quite ")
        else:
            raise ValueError(f"Game with id {old_game_id}, not found")


    # we are uploading new game by using UUID from data base, if game uploaded with finish state WIN and LOSE

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
                game_repo.save_fsm(game, old_game_id)
                # print(game.results())
                break
            if game.state == GameState.WON:
                print(result)
                game_repo.save_fsm(game, old_game_id)
                # print(game.results())
                break

        except KeyboardInterrupt:
            raise "Program Interrupted"

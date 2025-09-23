import random

############################ Storage of arrays ######################################
words_to_guess = {"easy": {"blazing": "rust", "superman": "famous comics hero"},
                  "medium": {"digital": "signal is analog or ....", "iqos": "smoke"},
                  "hard": {"iphone": "apple", "python": "so slow"}}

amount_to_guess = {"easy": 5, "medium": 3, "hard": 2}
counter = 0
string_storage = ""
greetings_tab = "Welcome to the hangman game!\ntype :help"
menus_tab = "1.Start_Game \n2.Start Random Game with Random Difficulty \n3.End_Game"
print(greetings_tab)


# progress_tab = []
############################ Support functions ######################################
def select_random_word(difficulty: str) -> tuple[str, str]:
    storage = {}
    for key, value in words_to_guess.items():
        if difficulty == key:
            for nested_key, nested_value in value.items():
                storage[nested_key] = nested_value
    hint, word = random.choice(list(storage.items()))
    return hint, word

def select_random_difficulty() -> str:
    difficulties = ["easy", "medium", "hard"]
    return random.choice(difficulties)


############################ Core Logic of Game ######################################
try:
    while True:
        terminal = input().lower()
        if terminal == "help":
            print(menus_tab)
            continue
        elif terminal == "1":
            print("Select_Difficulty: easy, medium, hard")
        elif terminal == "3":
            break
        elif terminal == "easy" or terminal == "medium" or terminal == "hard" or terminal == "2":
            if terminal == "2":
                terminal = select_random_difficulty()
            word, hint = select_random_word(terminal)
            print(f"Difficulty chose {terminal}")
            print(f"Guess the word: {hint}")
            print(f"Amount of guess left: {amount_to_guess[terminal] - counter}")

            while True:
                if string_storage != word:
                    if amount_to_guess[terminal] - counter != 0:
                        guess_word = input().lower()
                        if guess_word in word:
                            for number, letter in enumerate(word):
                                if letter is guess_word:
                                    string_storage[number] = letter
                            string_storage += guess_word
                            print(string_storage)
                            print(f"Correct letter: {guess_word}")
                            print(f"Amount of guess words left: {amount_to_guess[terminal] - counter}")
                        else:
                            counter += 1
                            print(f"Incorrect letter: {guess_word}")
                            print(f"Wrong, Amount of guess words left: {amount_to_guess[terminal] - counter}")
                    else:
                        print("You lost, try again later")
                        break
                else:
                    print("You won!, congrats")
                    break
            print("Game Finished, Hope you have enjoyed")
            break
        elif terminal == "":
            break

except KeyboardInterrupt:
    print("Program Interrupted")

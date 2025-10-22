import sqlite3
from cli import game_engine

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db")
        self.cursor = self.conn.cursor()

    def test_connection(self):
        try:
            if self.cursor:
                return "Connection successful!"
        except Exception as e:
            raise f"Database faced an error: {e}"

    def create_game_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Games( 
                            id TEXT,
                            player_id INTEGER,
                            guessed_word TEXT,
                            hint TEXT,
                            difficulty_level TEXT,
                            tries_left INTEGER,
                            last_state TEXT,
                            FOREIGN KEY (player_id) references Player(id))
                                ''')
            self.conn.commit()
        except Exception as e:
            raise f"Error type: {e}"

    def create_player_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                player_name TEXT
                                   )''')

            self.conn.commit()
        except Exception as e:
            raise f"Error type: {e}"

    def store_name(self, name):
        try:
            self.cursor.execute('''INSERT INTO Player(player_name)
            VALUES (?)''', (name,))

            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            raise f"Error type: {e}"

    def store_game(self, data):
        game, uuid = data[0], data[1]
        word_to_guess = game.player.selected_word
        hint = game.player.hint
        difficulty_level = game.level.name
        tries_left = game.player.tries_left
        last_state = game.state.name

        try:
            self.cursor.execute(''' INSERT INTO Games(
                                id,
                                player_id,
                                guessed_word,
                                hint,
                                difficulty_level,
                                tries_left,
                                last_state
                                ) VALUES (?,?,?,?,?,?,?)''',
                                 (str(uuid),
                                            self.cursor.lastrowid,
                                            word_to_guess,
                                            hint,
                                            difficulty_level,
                                            tries_left,
                                            last_state))
            self.conn.commit()
        except Exception as e:
            raise f"Error type: {e}"


    def get_name(self, id):
        try:
            data = self.cursor.execute('''  
                                       SELECT id, player_name FROM Player   
                                       WHERE id = ?''',(id,))

            for values in data:
                return values[1]
            self.cursor.close()
        except Exception as e:
            raise f"Error type: {e}"

    def get_game(self, uuid):
       try:
           data = self.cursor.execute('''SELECT * From Games
                                             WHERE id = ? ''',(uuid,))
           for values in data:
               return values[1:]
           self.cursor.close()
       except Exception as e:
           raise f"Error type: {e}"


# cp = DataBase()

# print(cp.create_player_table())
# print(cp.create_game_table())
# cp.store_name(data=game_engine())
# cp.store_game(data=game_engine())
# print(cp.get_name(1))
# print(cp.get_game("b98f2da5-d357-4ba0-a44a-a83eba677859"))


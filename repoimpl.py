import sqlite3
import uuid
from fsm import GameManager



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
        except BaseException as e:
            raise e

    def create_player_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                player_name TEXT
                                   )''')

            self.conn.commit()
        except BaseException as e:
            raise e

    def store_name(self, name):
        self.cursor.execute('''SELECT player_name FROM Player
                                            WHERE player_name = ?''', (name,))
        db_check_name = self.cursor.fetchone()

        if db_check_name is None:

            try:
                self.cursor.execute('''INSERT INTO Player(player_name)
                VALUES (?)''', (name,))

                self.conn.commit()
                return self.cursor.lastrowid
            except BaseException as e:
                raise e
        else:
            return None

    def store_game(self, data):
        game, uuid = data[0], data[1]
        word_to_guess = game.selected_word
        hint = game.hint
        difficulty_level = game.level.name
        tries_left = game.tries_left
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
        except BaseException as e:
            raise e


    def get_name(self, id):
        try:
            data = self.cursor.execute('''SELECT id, player_name FROM Player   
                                       WHERE id = ?''',(id,))
            for values in data:
                return values[1]
            self.cursor.close()
        except BaseException as e:
            raise e

    def get_game(self, game_id: uuid.UUID)-> GameManager | None:
       try:
           self.cursor.execute('''SELECT * From Games
                                             WHERE id = ? ''',(game_id,))
           export = self.cursor.fetchone()
           self.cursor.close()
           return GameManager(state=export[6], level=export[4])
       except BaseException as e:
           raise e

cp = DataBase()

# print(cp.create_player_table())
# print(cp.create_game_table())
# cp.store_name(data=game_engine())
# cp.store_game(data=game_engine())
# print(cp.get_name(1))
# print(cp.get_game("b98f2da5-d357-4ba0-a44a-a83eba677859"))
#
# ('b98f2da5-d357-4ba0-a44a-a83eba677859', None, 'python', 'so slow', 'HARD', 2, 'LOST')

print(cp.store_name("Kevin"))
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
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Game( 
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_id INTEGER,
                            guessed_word TEXT,
                            game_id BLOB,
                            games_won INTEGER,
                            games_lost INTEGER,
                            FOREIGN KEY (player_id) references Player(id))
                                ''')

            self.conn.commit()
        except Exception as e:
            print(e)

    def create_player_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                player_name TEXT
                                   )''')

            self.conn.commit()
        except Exception as e:
            print(e)


cp = DataBase()

print(cp.create_player_table())
print(cp.create_game_table())
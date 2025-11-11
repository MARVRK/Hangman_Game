import sqlite3
from fsm import GameManager, Player, GameState, Difficulty


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
                            id TEXT PRIMARY KEY ,
                            player_id INTEGER,
                            guessed_word TEXT,
                            output TEXT,
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

    def save_name(self, name):
        self.cursor.execute('''SELECT player_name FROM Player
                                   WHERE player_name = ?''', (name,))
        db_check_name = self.cursor.fetchone()

        if db_check_name is None:
            try:
                self.cursor.execute('''INSERT INTO Player(player_name)
                VALUES (?)''', (name,))

                self.conn.commit()
                return Player(id=self.cursor.lastrowid, player_name=name)
            except BaseException as e:
                raise e
        else:
            return None

    def get_name(self, id) -> Player | None:
        try:
            data = self.cursor.execute('''SELECT id, player_name FROM Player   
                                           WHERE id = ?''',(id,))
            if data:
                for value in data:
                    return Player(id=value[0], player_name=value[1])
            else:
                self.cursor.close()
                return None
        except BaseException as e:
            raise e

    def save_game(self, data: GameManager):
        id = data.id
        player_id = data.player_id
        word_to_guess = data.selected_word
        hint = data.hint
        difficulty_level = data.level.name
        tries_left = data.tries_left
        last_state = data.state.name
        # converting output list to one single string
        output = ""
        for letter in data.output:
            output += letter

        try:
                self.cursor.execute('''INSERT INTO Games(id,
                                      player_id,
                                      guessed_word,
                                      output,
                                      hint,
                                      difficulty_level,
                                      tries_left,
                                      last_state)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id)
                    DO UPDATE SET
                        player_id = EXCLUDED.player_id,
                        guessed_word = EXCLUDED.guessed_word,
                        output = EXCLUDED.output,
                        hint = EXCLUDED.hint,
                        difficulty_level = EXCLUDED.difficulty_level,
                        tries_left = EXCLUDED.tries_left,
                        last_state = EXCLUDED.last_state;
              ''', (str(id),
                              player_id,
                              word_to_guess,
                              output,
                              hint,
                              difficulty_level,
                              tries_left,
                              last_state))

                self.conn.commit()
        except BaseException as e:
            raise e

    def get_game(self, game_id: str)-> GameManager | None:
       try:
           self.cursor.execute('''SELECT * From Games
                                             WHERE id = ? ''',(game_id,))
           export = self.cursor.fetchone()
           if export is not None:
               return GameManager(id=export[0],
                                  player_id=export[1],
                                  selected_word=export[2],
                                  output=[x for x in export[3]],
                                  hint=export[4],
                                  level=Difficulty[export[5]],
                                  state=GameState[export[7]],
                                  tries_left=export[6])
           else:
               self.cursor.close()
               return None
       except BaseException as e:
           raise e

cp = DataBase()
# cp.create_game_table()
# cp.create_player_table()
# print(cp.get_name(id=1))
# print(cp.get_game(game_id="e93d243e-46bc-41ac-b357-2cde1d90b24b"))

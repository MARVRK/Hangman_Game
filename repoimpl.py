import sqlite3
from fsm import GameManager, Player



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

    # def create_game_table(self):
    #     try:
    #         self.cursor.execute('''CREATE TABLE IF NOT EXISTS Games(
    #                         id TEXT PRIMARY KEY ,
    #                         player_id INTEGER,
    #                         guessed_word TEXT,
    #                         hint TEXT,
    #                         difficulty_level TEXT,
    #                         tries_left INTEGER,
    #                         last_state TEXT,
    #                         FOREIGN KEY (player_id) references Player(id))
    #                             ''')
    #         self.conn.commit()
    #     except BaseException as e:
    #         raise e
    #
    # def create_player_table(self):
    #     try:
    #         self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player(
    #                             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             player_name TEXT
    #                                )''')
    #
    #         self.conn.commit()
    #     except BaseException as e:
    #         raise e

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

    def save_game(self, data, old_game_id):
        id = data.id
        player_id = data.player_id
        word_to_guess = data.selected_word
        hint = data.hint
        difficulty_level = data.level.name
        tries_left = data.tries_left
        last_state = data.state.name

        try:
            if old_game_id is None:
                self.cursor.execute(''' INSERT INTO Games(
                                id,
                                player_id,
                                guessed_word,
                                hint,
                                difficulty_level,
                                tries_left,
                                last_state
                                ) VALUES (?,?,?,?,?,?,?)''',
                                 (str(id),
                                            player_id,
                                            word_to_guess,
                                            hint,
                                            difficulty_level,
                                            tries_left,
                                            last_state))
                self.conn.commit()
            else:
                self.cursor.execute('''INSERT INTO Games(id,
                                      player_id,
                                      guessed_word,
                                      hint,
                                      difficulty_level,
                                      tries_left,
                                      last_state)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id)
                    DO UPDATE SET
                        player_id = EXCLUDED.player_id,
                        guessed_word = EXCLUDED.guessed_word,
                        hint = EXCLUDED.hint,
                        difficulty_level = EXCLUDED.difficulty_level,
                        tries_left = EXCLUDED.tries_left,
                        last_state = EXCLUDED.last_state;
              ''', (old_game_id,
                              player_id,
                              word_to_guess,
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
               return GameManager(game_id=export[0],
                                  player_id=export[1],
                                  hint=export[3],
                                  selected_word=export[2],
                                  level=export[4],
                                  state=export[6],
                                  tries_left=export[5])
           else:
               self.cursor.close()
               return None
       except BaseException as e:
           raise e

cp = DataBase()
# cp.create_game_table()
# cp.create_player_table()
# print(cp.get_name(id=1))
# print(cp.get_game(game_id="b98f2da5-d357-4ba0-a44a-a83eba677859"))


from fastapi.exceptions import HTTPException
import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(database="gamerepo.db")
        self.cursor = self.conn.cursor()

    def test_connection(self):
        try:
            if self.cursor:
                return "Connection successful!"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database faced an error: {e}")

    def create(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player( 
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_name TEXT,
                            games_won INTEGER,
                            games_lost INTEGER)''')

            self.conn.commit()
        except Exception as e:
            print(e)

cp = DataBase()
cp.create()
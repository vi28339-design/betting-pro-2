import sqlite3
import os

class DB:
    def __init__(self):
        self.db_path = os.path.join(os.path.expanduser("~"), "betting.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT, team1 TEXT, team2 TEXT, 
            line REAL, rec TEXT, created TEXT
        );
        """)
        self.conn.commit()

    def save_prediction(self, sport, t1, t2, line, rec):
        try:
            self.conn.execute(
                "INSERT INTO history (sport, team1, team2, line, rec, created) VALUES (?,?,?,?,?,datetime('now'))",
                (sport, t1, t2, line, rec)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка БД: {e}")

db = DB()

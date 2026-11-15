import sqlite3
import os

class DB:
    def __init__(self, app_paths):
        # ✅ Берем папку documents, она точно доступна
        self.data_dir = app_paths.documents
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception:
            pass # Если не удалось создать, попробуем использовать как есть
            
        self.db_path = os.path.join(str(self.data_dir), "betting.db")
        
        # ✅ Приводим к str, чтобы sqlite3 не ругался на Path
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._init()

    def _init(self):
        try:
            c = self.conn.cursor()
            c.executescript("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sport TEXT, team1 TEXT, team2 TEXT, 
                line REAL, rec TEXT, created TEXT
            );
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")

    def save_prediction(self, sport, t1, t2, line, rec):
        try:
            self.conn.execute(
                "INSERT INTO history (sport, team1, team2, line, rec, created) VALUES (?,?,?,?,?,datetime('now'))",
                (sport, t1, t2, line, rec)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка БД: {e}")

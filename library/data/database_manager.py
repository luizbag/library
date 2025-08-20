import sqlite3
from pathlib import Path

class DatabaseManager:
    _instance = None
    _connection = None
    _db_path = None

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            if db_path is None:
                app_data_dir = Path.home() / '.library-app'
                cls._db_path = app_data_dir / 'library.db'
            else:
                cls._db_path = Path(db_path)
            
            cls._ensure_db_directory_exists()
            cls._connection = cls._get_db_connection()
            cls._connection.row_factory = sqlite3.Row
        return cls._instance

    @classmethod
    def _ensure_db_directory_exists(self):
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_db_connection(self):
        try:
            return sqlite3.connect(self._db_path)
        except sqlite3.Error as e:
            raise RuntimeError(f"Database connection error: {e}")

    @property
    def connection(self):
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            self._instance = None
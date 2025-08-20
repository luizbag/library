import sqlite3
from .database_manager import DatabaseManager

class BaseRepository:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager
        self.conn = self._db_manager.connection
        self._create_tables()

    def _create_tables(self):
        raise NotImplementedError("Subclasses must implement the _create_tables method.")
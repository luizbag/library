import sqlite3
from typing import List

from library.models import Person
from library.data.base_repository import BaseRepository

class PersonRepository(BaseRepository):
    """
    Handles all data access for Person objects using SQLite.
    """

    def _create_tables(self):
        """
        Creates the 'people' table if it doesn't exist.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS people (
                    name TEXT PRIMARY KEY,
                    phone_number TEXT
                )
            """)

    def add_person(self, person: Person):
        """
        Adds a new person to the database.
        """
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO people (name, phone_number) VALUES (?, ?)",
                    (person.name, person.phone_number)
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"Person with name '{person.name}' already exists.")

    def get_person_by_name(self, name: str) -> Person:
        """
        Fetches a person by their name.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM people WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return Person(
                    name=row['name'],
                    phone_number=row['phone_number']
                )
            return None

    def update_person(self, old_name: str, new_name: str = None, new_phone_number: str = None):
        """
        Updates a person's name and/or phone number.
        """
        updates = []
        params = []
        if new_name is not None:
            updates.append("name = ?")
            params.append(new_name)
        if new_phone_number is not None:
            updates.append("phone_number = ?")
            params.append(new_phone_number)
        
        if not updates:
            return

        query = f"UPDATE people SET {', '.join(updates)} WHERE name = ?"
        params.append(old_name)
        
        try:
            with self.conn:
                self.conn.execute(query, tuple(params))
        except sqlite3.IntegrityError:
            raise ValueError(f"Could not update. Name '{new_name}' already exists.")

    def get_all_people(self) -> List[Person]:
        """
        Fetches all people from the database.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM people")
            rows = cursor.fetchall()
            return [
                Person(
                    name=row['name'],
                    phone_number=row['phone_number']
                ) for row in rows
            ]
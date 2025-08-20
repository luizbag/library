import sqlite3
from typing import List

from library.models.models import Person
from library.data.base_repository import BaseRepository

class PersonRepository(BaseRepository):
    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone_number TEXT
                )
            """)

    def add_person(self, person: Person) -> Person:
        """
        Adds a new person to the database and returns the person with their new ID.
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO people (name, phone_number) VALUES (?, ?)",
                    (person.name, person.phone_number)
                )
                new_id = cursor.lastrowid
                
                return Person(
                    id=new_id,
                    name=person.name,
                    phone_number=person.phone_number
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"Person with name '{person.name}' already exists.")


    def get_person_by_id(self, person_id: int) -> Person:
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM people WHERE id = ?", (person_id,))
            row = cursor.fetchone()
            if row:
                return Person(name=row['name'], phone_number=row['phone_number'], id=row['id'])
            return None

    def get_person_by_name(self, name: str) -> Person:
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM people WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return Person(name=row['name'], phone_number=row['phone_number'], id=row['id'])
            return None

    def update_person(self, person_id: int, new_name: str = None, new_phone_number: str = None):
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

        query = f"UPDATE people SET {', '.join(updates)} WHERE id = ?"
        params.append(person_id)
        
        try:
            with self.conn:
                cursor = self.conn.execute(query, tuple(params))
                # Check the number of affected rows
                if cursor.rowcount == 0:
                    raise ValueError(f"Person with ID '{person_id}' not found.")
        except sqlite3.IntegrityError:
            raise ValueError(f"Could not update. Name '{new_name}' already exists.")


    def get_all_people(self) -> List[Person]:
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM people")
            rows = cursor.fetchall()
            return [Person(name=row['name'], phone_number=row['phone_number'], id=row['id']) for row in rows]
import sqlite3
from typing import List

from library.models.models import Book
from library.data.base_repository import BaseRepository

class BookRepository(BaseRepository):
    """
    Handles all data access for Book objects using SQLite.
    """

    def _create_tables(self):
        """
        Creates the 'books' table with an auto-incrementing primary key.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    isbn TEXT NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    is_available INTEGER NOT NULL
                )
            """)

    def add_book(self, book: Book) -> Book:
        """
        Adds a new book to the database and returns the book with its new ID.
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO books (isbn, title, author, is_available) VALUES (?, ?, ?, ?)",
                    (book.isbn, book.title, book.author, int(book.is_available))
                )
                new_id = cursor.lastrowid
                
                # Return the Book object with the newly assigned ID
                return Book(
                    id=new_id,
                    title=book.title,
                    author=book.author,
                    isbn=book.isbn,
                    is_available=book.is_available
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"Book with ISBN '{book.isbn}' already exists.")

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Fetches a book by its auto-generated ID.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return Book(
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    is_available=bool(row['is_available']),
                    id=row['id']
                )
            return None

    def get_book_by_isbn(self, isbn: str) -> Book:
        """
        Fetches a book by its ISBN.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
            row = cursor.fetchone()
            if row:
                return Book(
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    is_available=bool(row['is_available']),
                    id=row['id']
                )
            return None

    def update_book_availability(self, book_id: int, is_available: bool):
        """
        Updates the availability status of a book by its ID.
        """
        with self.conn:
            self.conn.execute(
                "UPDATE books SET is_available = ? WHERE id = ?",
                (int(is_available), book_id)
            )

    def get_all_books(self) -> List[Book]:
        """
        Fetches all books from the database.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [
                Book(
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    is_available=bool(row['is_available']),
                    id=row['id']
                ) for row in rows
            ]
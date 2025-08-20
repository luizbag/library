# my_books/data/book_repository.py
import sqlite3
from typing import List

from ..models import Book
from .base_repository import BaseRepository
from .database_manager import DatabaseManager

class BookRepository(BaseRepository):
    """
    Handles all data access for Book objects using SQLite.
    """
    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    def _create_tables(self):
        """
        Creates the 'books' table if it doesn't exist.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    is_available INTEGER NOT NULL
                )
            """)

    def add_book(self, book: Book):
        """
        Adds a new book to the database.
        """
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO books (isbn, title, author, is_available) VALUES (?, ?, ?, ?)",
                    (book.isbn, book.title, book.author, int(book.is_available))
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"Book with ISBN '{book.isbn}' already exists.")

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
                    is_available=bool(row['is_available'])
                )
            return None

    def search_books_by_title(self, search_term: str) -> List[Book]:
        """
        Fetches books from the database with a title containing the search term.
        """
        with self.conn:
            cursor = self.conn.execute(
                "SELECT * FROM books WHERE title LIKE ?",
                (f"%{search_term}%",)
            )
            rows = cursor.fetchall()
            return [
                Book(
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    is_available=bool(row['is_available'])
                ) for row in rows
            ]

    def update_book_availability(self, isbn: str, is_available: bool):
        """
        Updates the availability status of a book.
        """
        with self.conn:
            self.conn.execute(
                "UPDATE books SET is_available = ? WHERE isbn = ?",
                (int(is_available), isbn)
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
                    is_available=bool(row['is_available'])
                ) for row in rows
            ]
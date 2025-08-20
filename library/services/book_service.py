# library/services/book_service.py

from typing import List
from library.models.models import Book
from library.data.book_repository import BookRepository

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def add_new_book(self, title: str, author: str, isbn: str) -> Book:
        if not all([title, author, isbn]):
            raise ValueError("Title, author, and ISBN cannot be empty.")
            
        new_book = Book(title, author, isbn)
        return self.book_repository.add_book(new_book)

    def get_book_by_id(self, book_id: int) -> Book:
        return self.book_repository.get_book_by_id(book_id)

    def get_book_by_isbn(self, isbn: str) -> Book:
        """
        Retrieves a book by its ISBN from the repository.
        """
        return self.book_repository.get_book_by_isbn(isbn)

    def get_all_books(self) -> List[Book]:
        return self.book_repository.get_all_books()

    def search_books(self, search_term: str) -> List[Book]:
        return self.book_repository.search_books(search_term)
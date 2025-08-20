from typing import List

from ..models import Book
from ..data.book_repository import BookRepository

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def add_new_book(self, title: str, author: str, isbn: str) -> Book:
        """
        Validates book data and adds a new book to the library.
        
        Args:
            title: The title of the book.
            author: The author of the book.
            isbn: The ISBN of the book.
        
        Returns:
            The newly created Book object.
        
        Raises:
            ValueError: If any required field is empty or if a book with the
                        same ISBN already exists.
        """
        if not title or not author or not isbn:
            raise ValueError("Title, author, and ISBN cannot be empty.")
        
        new_book = Book(title, author, isbn)
        self.book_repository.add_book(new_book)
        return new_book

    def get_all_books(self) -> List[Book]:
        """
        Retrieves all books from the library.
        
        Returns:
            A list of all Book objects.
        """
        return self.book_repository.get_all_books()
    
    def get_book_by_isbn(self, isbn: str) -> Book:
        """
        Retrieves a single book by its ISBN.
        
        Args:
            isbn: The ISBN of the book to retrieve.
        
        Returns:
            The Book object, or None if not found.
        """
        if not isbn:
            raise ValueError("ISBN cannot be empty.")
            
        return self.book_repository.get_book_by_isbn(isbn)

    def search_books_by_title(self, search_term: str) -> List[Book]:
        """
        Searches for books with a title containing the search term.
        
        Args:
            search_term: The term to search for.
            
        Returns:
            A list of matching Book objects.
        """
        if not search_term:
            raise ValueError("Search term cannot be empty.")
            
        return self.book_repository.search_books_by_title(search_term)
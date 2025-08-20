import pytest
from unittest.mock import Mock
from library.models.models import Book
from library.services.book_service import BookService

@pytest.fixture
def book_service():
    """Provides a BookService instance with a mocked repository."""
    mock_repo = Mock()
    return BookService(mock_repo)

def test_add_new_book_success(book_service):
    """Tests a successful book addition."""
    # The repository's add_book method should return the book with an ID from the database
    book_service.book_repository.add_book.return_value = Book(id=1, title="Mock Title", author="Mock Author", isbn="mock-isbn")
    new_book = book_service.add_new_book("Mock Title", "Mock Author", "mock-isbn")
    assert new_book.title == "Mock Title"
    assert new_book.id == 1
    book_service.book_repository.add_book.assert_called_once()

def test_add_new_book_with_empty_fields_raises_error(book_service):
    """Tests that adding a book with empty fields raises a ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        book_service.add_new_book("", "Author", "isbn")
    book_service.book_repository.add_book.assert_not_called()
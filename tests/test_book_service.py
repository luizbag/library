import pytest
from unittest.mock import Mock
from library.models import Book
from library.services.book_service import BookService

@pytest.fixture
def book_service():
    """Provides a BookService instance with a mocked repository."""
    mock_repo = Mock()
    return BookService(mock_repo)

def test_add_new_book_success(book_service):
    """Tests successful book addition via the service."""
    book_service.book_repository.add_book.return_value = None
    new_book = book_service.add_new_book("Mock Title", "Mock Author", "mock-isbn")
    assert new_book.title == "Mock Title"
    book_service.book_repository.add_book.assert_called_once()

def test_add_new_book_with_empty_fields_raises_error(book_service):
    """Tests that adding a book with empty fields raises a ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        book_service.add_new_book("", "Author", "isbn")
    book_service.book_repository.add_book.assert_not_called()

def test_add_new_book_that_already_exists_raises_error(book_service):
    """Tests that trying to add a book with an existing ISBN raises an error."""
    book_service.book_repository.add_book.side_effect = ValueError("already exists")
    with pytest.raises(ValueError, match="already exists"):
        book_service.add_new_book("Existing Book", "Author", "existing-isbn")
    book_service.book_repository.add_book.assert_called_once()
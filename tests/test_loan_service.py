import pytest
from unittest.mock import Mock, patch
from library.services.loan_service import LoanService
from library.models.models import Book, Person, Loan
from datetime import datetime, timedelta

@pytest.fixture
def loan_service():
    """Provides a LoanService with mocked dependencies."""
    mock_loan_repo = Mock()
    mock_book_repo = Mock()
    mock_person_repo = Mock()
    return LoanService(mock_loan_repo, mock_book_repo, mock_person_repo)

def test_lend_book_success(loan_service):
    """Tests a successful book lending transaction."""
    mock_book = Book(id=1, title="Mock Book", author="Mock Author", isbn="mock-isbn", is_available=True)
    mock_person = Person(id=1, name="Mock Person", phone_number="123-456-7890")
    
    loan_service.book_repository.get_book_by_id.return_value = mock_book
    loan_service.person_repository.get_person_by_id.return_value = mock_person
    loan_service.loan_repository.add_loan.return_value = Loan(id=1, book_id=1, person_id=1, loan_date=datetime(2025, 1, 1), due_date=datetime(2025, 1, 15))

    with patch("library.services.loan_service.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 1, 1)
        loan = loan_service.lend_book(1, 1)
        
    assert loan.person_id == 1
    assert loan.book_id == 1
    assert loan.due_date == datetime(2025, 1, 15)
    
    loan_service.book_repository.update_book_availability.assert_called_with(1, is_available=False)
    loan_service.loan_repository.add_loan.assert_called_once()

def test_lend_nonexistent_book_raises_error(loan_service):
    """Tests that lending a non-existent book raises a ValueError."""
    loan_service.book_repository.get_book_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Book with ID '999' not found."):
        loan_service.lend_book(999, 1)

def test_lend_unavailable_book_raises_error(loan_service):
    """Tests that lending an unavailable book raises a ValueError."""
    mock_book = Book(id=1, title="Mock Book", author="Mock Author", isbn="mock-isbn", is_available=False)
    loan_service.book_repository.get_book_by_id.return_value = mock_book
    
    with pytest.raises(ValueError, match="is currently not available"):
        loan_service.lend_book(1, 1)
        
    loan_service.book_repository.update_book_availability.assert_not_called()

def test_lend_to_nonexistent_person_raises_error(loan_service):
    """Tests that lending a book to a non-existent person raises a ValueError."""
    mock_book = Book(id=1, title="Mock Book", author="Mock Author", isbn="mock-isbn", is_available=True)
    loan_service.book_repository.get_book_by_id.return_value = mock_book
    loan_service.person_repository.get_person_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Person with ID '999' not found."):
        loan_service.lend_book(1, 999)

def test_return_book_success(loan_service):
    """Tests a successful book return."""
    mock_book = Book(id=1, title="Mock Book", author="Mock Author", isbn="mock-isbn", is_available=False)
    loan_service.book_repository.get_book_by_id.return_value = mock_book
    
    loan_service.return_book(1)
    
    loan_service.book_repository.update_book_availability.assert_called_with(1, is_available=True)
    loan_service.loan_repository.remove_loan_by_book_id.assert_called_with(1)

def test_return_nonexistent_book_raises_error(loan_service):
    """Tests that returning a non-existent book raises a ValueError."""
    loan_service.book_repository.get_book_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Book with ID '999' not found."):
        loan_service.return_book(999)

def test_return_available_book_raises_error(loan_service):
    """Tests that returning an already available book raises a ValueError."""
    mock_book = Book(id=1, title="Mock Book", author="Mock Author", isbn="mock-isbn", is_available=True)
    loan_service.book_repository.get_book_by_id.return_value = mock_book
    
    with pytest.raises(ValueError, match="is already available"):
        loan_service.return_book(1)
        
    loan_service.book_repository.update_book_availability.assert_not_called()
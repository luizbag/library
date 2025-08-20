from datetime import datetime, timedelta
from library.data.loan_repository import LoanRepository
from library.data.book_repository import BookRepository
from library.data.person_repository import PersonRepository
from library.models.models import Loan, Book, Person

class LoanService:
    def __init__(self, loan_repository: LoanRepository, book_repository: BookRepository, person_repository: PersonRepository):
        self.loan_repository = loan_repository
        self.book_repository = book_repository
        self.person_repository = person_repository

    def lend_book(self, book_id: int, person_id: int, loan_period_days: int = 14) -> Loan:
        """
        Handles the process of lending a book to a person.
        
        Args:
            book_id: The ID of the book to be lent.
            person_id: The ID of the person borrowing the book.
            loan_period_days: The number of days the loan is for.
        
        Returns:
            The created Loan object.
        
        Raises:
            ValueError: If the book is not found, not available, or the person is not found.
        """
        book: Book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with ID '{book_id}' not found.")
        if not book.is_available:
            raise ValueError(f"Book with ID '{book_id}' is currently not available.")
            
        person: Person = self.person_repository.get_person_by_id(person_id)
        if person is None:
            raise ValueError(f"Person with ID '{person_id}' not found.")
            
        self.book_repository.update_book_availability(book_id, is_available=False)
        
        loan_date = datetime.now()
        due_date = loan_date + timedelta(days=loan_period_days)
        new_loan = Loan(book_id, person_id, loan_date, due_date)
        return self.loan_repository.add_loan(new_loan)

    def return_book(self, book_id: int):
        """
        Handles the process of returning a book.
        
        Args:
            book_id: The ID of the book to be returned.
        
        Raises:
            ValueError: If the book is already available or no loan record is found.
        """
        book: Book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with ID '{book_id}' not found.")
        if book.is_available:
            raise ValueError(f"Book with ID '{book_id}' is already available.")
            
        self.book_repository.update_book_availability(book_id, is_available=True)
        self.loan_repository.remove_loan_by_book_id(book_id)
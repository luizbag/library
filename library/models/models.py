from dataclasses import dataclass
from datetime import datetime

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    is_available: bool = True
    id: int = None  # New primary key

@dataclass
class Person:
    name: str
    phone_number: str
    id: int = None  # New field for a unique ID

@dataclass
class Loan:
    book_id: str
    person_id: int  # Changed from `borrower_name` to `person_id`
    loan_date: datetime
    due_date: datetime
    id: int = None
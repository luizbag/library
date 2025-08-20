from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, is_available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_available": self.is_available
        }

class Person:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def to_dict(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number
        }

class Loan:
    def __init__(self, isbn, borrower_name, loan_date, due_date):
        self.isbn = isbn
        self.borrower_name = borrower_name
        self.loan_date = loan_date
        self.due_date = due_date

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "borrower_name": self.borrower_name,
            "loan_date": self.loan_date.strftime("%Y-%m-%d"),
            "due_date": self.due_date.strftime("%Y-%m-%d")
        }
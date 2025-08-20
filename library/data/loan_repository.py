import sqlite3
from typing import List

from library.models.models import Loan
from library.data.base_repository import BaseRepository
from datetime import datetime

class LoanRepository(BaseRepository):
    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER UNIQUE NOT NULL,
                    borrower_id INTEGER NOT NULL,
                    loan_date TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (borrower_id) REFERENCES people(id)
                )
            """)

    def add_loan(self, loan: Loan) -> Loan:
        """
        Adds a new loan record to the database and returns the loan with its new ID.
        """
        try:
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO loans (book_id, borrower_id, loan_date, due_date) VALUES (?, ?, ?, ?)",
                    (loan.book_id, loan.person_id, loan.loan_date.strftime("%Y-%m-%d"), loan.due_date.strftime("%Y-%m-%d"))
                )
                new_id = cursor.lastrowid

                return Loan(
                    id=new_id,
                    book_id=loan.book_id,
                    person_id=loan.person_id,
                    loan_date=loan.loan_date,
                    due_date=loan.due_date
                )
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                raise ValueError("Borrower ID or Book ID does not exist.")
            raise ValueError(f"Loan record for Book ID '{loan.book_id}' already exists.")

            
    def get_loan_by_id(self, loan_id: int) -> Loan:
        """
        Fetches a loan record by its unique ID.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
            row = cursor.fetchone()
            if row:
                return Loan(
                    book_id=row['book_id'],
                    person_id=row['borrower_id'],
                    loan_date=datetime.strptime(row['loan_date'], "%Y-%m-%d"),
                    due_date=datetime.strptime(row['due_date'], "%Y-%m-%d"),
                    id=row['id']
                )
            return None

    def get_loan_by_book_id(self, book_id: int) -> Loan:
        """
        Fetches a loan record by the book's ID.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM loans WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return Loan(
                    book_id=row['book_id'],
                    person_id=row['borrower_id'],
                    loan_date=datetime.strptime(row['loan_date'], "%Y-%m-%d"),
                    due_date=datetime.strptime(row['due_date'], "%Y-%m-%d"),
                    id=row['id']
                )
            return None

    def get_loans_by_person_id(self, person_id: int) -> List[Loan]:
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM loans WHERE borrower_id = ?", (person_id,))
            rows = cursor.fetchall()
            return [
                Loan(
                    book_id=row['book_id'],
                    person_id=row['borrower_id'],
                    loan_date=datetime.strptime(row['loan_date'], "%Y-%m-%d"),
                    due_date=datetime.strptime(row['due_date'], "%Y-%m-%d"),
                    id=row['id']
                ) for row in rows
            ]

    def get_all_loans(self) -> List[Loan]:
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM loans")
            rows = cursor.fetchall()
            return [
                Loan(
                    book_id=row['book_id'],
                    person_id=row['borrower_id'],
                    loan_date=datetime.strptime(row['loan_date'], "%Y-%m-%d"),
                    due_date=datetime.strptime(row['due_date'], "%Y-%m-%d"),
                    id=row['id']
                ) for row in rows
            ]

    def remove_loan_by_book_id(self, book_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM loans WHERE book_id = ?", (book_id,))
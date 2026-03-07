from typing import Dict, List
from datetime import date
from .models import Book, Member, BorrowRecord, FinePolicy

class Library:
    def __init__(self, fine_policy: FinePolicy):
        self.fine_policy = fine_policy
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.records: List[BorrowRecord] = []

    def add_book(self, book_id: str, title: str, author: str) -> None:
        # Unique ID check, then add Book
        if book_id in self.books:
            raise ValueError(f"Book ID '{book_id}' already exists.")
        self.books[book_id] = Book(book_id, title, author)

    def add_member(self, member_id: str, name: str) -> None:
        # Unique ID check, then add Member
        if member_id in self.members:
            raise ValueError(f"Member ID '{member_id}' already exists.")
        self.members[member_id] = Member(member_id, name)

    def borrow_book(self, member_id: str, book_id: str, borrow_date: date) -> None:
        # 1) Validate IDs exist
        if member_id not in self.members:
            raise KeyError(f"Member ID '{member_id}' not found.")
        if book_id not in self.books:
            raise KeyError(f"Book ID '{book_id}' not found.")

        member = self.members[member_id]
        book = self.books[book_id]

        # 2) book.borrow()
        book.borrow()
        
        # 3) member.borrow_book(book_id)
        try:
            member.borrow_book(book_id)
        except ValueError as e:
            book.return_book() # Rollback book status if member limit reached
            raise e

        # 4) Append BorrowRecord
        self.records.append(BorrowRecord(member_id, book_id, borrow_date))

    def return_book(self, member_id: str, book_id: str, return_date: date) -> float:
        # 1) Validate IDs exist
        if member_id not in self.members:
            raise KeyError(f"Member ID '{member_id}' not found.")
        if book_id not in self.books:
            raise KeyError(f"Book ID '{book_id}' not found.")

        member = self.members[member_id]
        book = self.books[book_id]

        # 2) member.return_book(book_id)
        member.return_book(book_id)

        # 3) book.return_book()
        book.return_book()

        # 4) Find open record and close it (set return_date)
        open_record = None
        for record in reversed(self.records):
            if record.member_id == member_id and record.book_id == book_id and record.return_date is None:
                open_record = record
                break
        
        if not open_record:
            raise ValueError("No open borrow record found.")
            
        open_record.return_date = return_date

        # 5) Compute fine using policy and return it (assume 7 days grace period per requirements)
        days_borrowed = (return_date - open_record.borrow_date).days
        days_late = max(0, days_borrowed - 7)
        return self.fine_policy.calculate(days_late)
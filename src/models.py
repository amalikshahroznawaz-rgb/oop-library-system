from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Optional
from abc import ABC, abstractmethod
from datetime import date

# --- Policy (Abstraction) ---
class FinePolicy(ABC):
    @abstractmethod
    def calculate(self, days_late: int) -> float:
        pass

class SimpleFinePolicy(FinePolicy):
    def __init__(self, per_day: float = 5.0):
        self.per_day = per_day

    def calculate(self, days_late: int) -> float:
        # Return fine for late days (no negative fines)
        if days_late <= 0:
            return 0.0
        return self.per_day * days_late

# --- Data Models ---
@dataclass
class Book:
    book_id: str
    title: str
    author: str
    _available: bool = field(default=True, repr=False)

    def borrow(self) -> None:
        # If not available -> raise ValueError
        if not self._available:
            raise ValueError(f"Book '{self.title}' is currently unavailable.")
        # Set available = False
        self._available = False

    def return_book(self) -> None:
        # Set available = True
        self._available = True

    def is_available(self) -> bool:
        return self._available

@dataclass
class Member:
    member_id: str
    name: str
    _borrowed_books: Set[str] = field(default_factory=set, repr=False)

    def borrow_book(self, book_id: str, limit: int = 3) -> None:
        # Enforce limit, then add. (Limit is at most 3 books)
        if len(self._borrowed_books) >= limit:
            raise ValueError(f"Member '{self.name}' has reached the borrow limit of {limit}.")
        self._borrowed_books.add(book_id)

    def return_book(self, book_id: str) -> None:
        # Validate membership, then remove
        if book_id not in self._borrowed_books:
            raise ValueError(f"Book '{book_id}' is not borrowed by member '{self.name}'.")
        self._borrowed_books.remove(book_id)

    @property
    def borrowed_books(self) -> Set[str]:
        # Return safe copy
        return set(self._borrowed_books)

@dataclass
class BorrowRecord:
    member_id: str
    book_id: str
    borrow_date: date
    return_date: Optional[date] = None
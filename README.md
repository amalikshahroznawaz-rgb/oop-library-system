# OOP Library System

A complete Library Management System implementing Encapsulation, Composition, and Abstraction.

## OOP Concepts Used
* **Encapsulation**: Book availability and member borrowing history are hidden behind private variables (`_available`, `_borrowed_books`).
* **Composition**: `Library` handles `Book`, `Member`, and `BorrowRecord` objects.
* **Abstraction**: Calculation of late fines relies on the `FinePolicy` interface.

## Running the CLI
```bash
python cli.py
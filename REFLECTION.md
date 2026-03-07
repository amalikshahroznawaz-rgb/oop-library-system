# Project Reflection & SOLID Principles

## 1. SOLID Principles Applied
I focused heavily on the **Single Responsibility Principle (SRP)** and **Separation of Concerns**. The `cli.py` file handles all the `print()` and `input()` statements, while the `models.py` and `services.py` files only handle data and borrowing rules. This made the code much easier to write unit tests for.

## 2. Which OOP Concept was the Hardest?
**Encapsulation** was a great learning curve here. Figuring out exactly which attributes should be private (like a book's availability status) and ensuring they were only modified through specific methods (like `borrow_book` or `return_book`) took careful planning.

## 3. What Design Mistakes Did I Make Initially?
My biggest initial mistake was the temptation to put `print()` statements directly inside my business logic classes. I quickly realized that doing this tightly couples the UI to the backend, making it impossible to write automated Unit Tests. I refactored the code to `raise ValueError` instead.

## 4. What Would I Improve?
If I were to expand this, I would improve the data persistence. Currently, everything is stored in in-memory dictionaries, meaning all data is lost when the program closes. I would improve this by integrating an SQLite database or saving the state to a JSON file.
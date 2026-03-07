import unittest
from datetime import date
from src.models import SimpleFinePolicy
from services import Library

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library = Library(SimpleFinePolicy(per_day=5.0))
        self.library.add_book("1", "Python Crash Course", "Eric Matthes")
        self.library.add_book("2", "Clean Code", "Robert C. Martin")
        self.library.add_book("3", "Fluent Python", "Luciano Ramalho")
        self.library.add_book("4", "Design Patterns", "GoF")
        self.library.add_member("M1", "Alice")

    def test_1_add_duplicate_book_raises_error(self):
        with self.assertRaises(ValueError):
            self.library.add_book("1", "Duplicate Book", "Author")

    def test_2_add_duplicate_member_raises_error(self):
        with self.assertRaises(ValueError):
            self.library.add_member("M1", "Duplicate Alice")

    def test_3_borrow_book_success(self):
        self.library.borrow_book("M1", "1", date(2023, 1, 1))
        self.assertFalse(self.library.books["1"].is_available())
        self.assertIn("1", self.library.members["M1"].borrowed_books)

    def test_4_borrow_unavailable_book_fails(self):
        self.library.borrow_book("M1", "1", date(2023, 1, 1))
        self.library.add_member("M2", "Bob")
        with self.assertRaises(ValueError): # Should fail because M1 has it
            self.library.borrow_book("M2", "1", date(2023, 1, 2))

    def test_5_borrow_limit_reached(self):
        self.library.borrow_book("M1", "1", date(2023, 1, 1))
        self.library.borrow_book("M1", "2", date(2023, 1, 1))
        self.library.borrow_book("M1", "3", date(2023, 1, 1))
        with self.assertRaises(ValueError): # 4th book should fail
            self.library.borrow_book("M1", "4", date(2023, 1, 1))

    def test_6_return_book_success_no_fine(self):
        self.library.borrow_book("M1", "1", date(2023, 1, 1))
        fine = self.library.return_book("M1", "1", date(2023, 1, 7)) # Returned exactly on 7th day
        self.assertEqual(fine, 0.0)
        self.assertTrue(self.library.books["1"].is_available())

    def test_7_return_not_borrowed_book_fails(self):
        with self.assertRaises(ValueError):
            self.library.return_book("M1", "2", date(2023, 1, 1))

    def test_8_fine_calculation_deterministic(self):
        self.library.borrow_book("M1", "1", date(2023, 1, 1))
        # Returned on Jan 11 (10 days total). Grace = 7. Late = 3. Fine = 3 * 5.0 = 15.0
        fine = self.library.return_book("M1", "1", date(2023, 1, 11))
        self.assertEqual(fine, 15.0)

if __name__ == '__main__':
    unittest.main()
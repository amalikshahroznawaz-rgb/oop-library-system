from datetime import date
from src.models import SimpleFinePolicy
from src.library import Library

def main():
    library = Library(SimpleFinePolicy(per_day=5.0))

    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")
        
        choice = input("Enter choice: ")

        try:
            if choice == '1':
                b_id = input("Enter Book ID: ")
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                library.add_book(b_id, title, author)
                print("Success: Book added!")

            elif choice == '2':
                m_id = input("Enter Member ID: ")
                name = input("Enter Name: ")
                library.add_member(m_id, name)
                print("Success: Member added!")

            elif choice == '3':
                m_id = input("Enter Member ID: ")
                b_id = input("Enter Book ID: ")
                library.borrow_book(m_id, b_id, date.today())
                print(f"Success: Book '{b_id}' borrowed by '{m_id}'.")

            elif choice == '4':
                m_id = input("Enter Member ID: ")
                b_id = input("Enter Book ID: ")
                fine = library.return_book(m_id, b_id, date.today())
                print(f"Success: Book returned! Total fine to pay: ${fine:.2f}")

            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

        except (ValueError, KeyError) as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
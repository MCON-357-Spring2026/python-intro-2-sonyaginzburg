"""
Exercise 4: Mini-Project - Library Management System
=====================================================
Combine everything: functions, classes, files, and JSON

This exercise brings together all the concepts from the course.
Build a simple library system that tracks books and borrowers.

Instructions:
- Complete all TODOs
- The system should persist data to JSON files
- Run this file to test your implementation

Run with: python exercise_4_project.py
"""

import json
import os
from datetime import datetime


# =============================================================================
# PART 1: HELPER FUNCTIONS
# =============================================================================

def format_date(dt: datetime = None) -> str:
    """
    Format a datetime object as a string "YYYY-MM-DD".
    If no datetime provided, use current date.

    Example:
        format_date(datetime(2024, 1, 15)) -> "2024-01-15"
        format_date() -> "2024-02-04" (today's date)
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


def generate_id(prefix: str, existing_ids: list) -> str:
    """
    Generate a new unique ID with the given prefix.

    Parameters:
        prefix: String prefix (e.g., "BOOK", "USER")
        existing_ids: List of existing IDs to avoid duplicates

    Returns:
        New ID in format "{prefix}_{number:04d}"

    Example:
        generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) -> "BOOK_0003"
        generate_id("USER", []) -> "USER_0001"
    """
    if not existing_ids:
        return f"{prefix}_0001"

    numbers = [
            int(i.split("_")[1])
            for i in existing_ids
            if i.startswith(prefix + "_")
    ]
    next_number = max(numbers, default = 0) + 1
    return f"{prefix}_{next_number:04d}"


def search_items(items: list, **criteria) -> list:
    """
    Search a list of dictionaries by matching criteria.
    Uses **kwargs to accept any search fields.

    Parameters:
        items: List of dictionaries to search
        **criteria: Field-value pairs to match (case-insensitive for strings)

    Returns:
        List of matching items

    Example:
        books = [
            {"title": "Python 101", "author": "Smith"},
            {"title": "Java Guide", "author": "Smith"},
            {"title": "Python Advanced", "author": "Jones"}
        ]
        search_items(books, author="Smith") -> [first two books]
        search_items(books, title="Python 101") -> [first book]
    """
    #  Implement this function
    results = []
    for item in items:
        match = True
        for key, value in criteria.items():
            if key not in item:
                match = False
                break
            item_value = item[key]
            if isinstance(item_value, str) and isinstance(value, str):
                if item_value.lower() != value.lower():
                    match = False
                    break
            else:
                if item_value != value:
                    match = False
                    break
        if match:
            results.append(item)
        return results


# =============================================================================
# PART 2: BOOK CLASS
# =============================================================================

class Book:
    """
    Represents a book in the library.

    Class Attributes:
        GENRES: List of valid genres ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    Instance Attributes:
        book_id (str): Unique identifier
        title (str): Book title
        author (str): Author name
        genre (str): Must be one of GENRES
        available (bool): Whether book is available for borrowing

    Methods:
        to_dict(): Convert to dictionary for JSON serialization
        from_dict(data): Class method to create Book from dictionary
        __str__(): Return readable string representation
    """

    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    def __init__(self, book_id: str, title: str, author: str, genre: str, available: bool = True):
        #  Initialize attributes
        if genre not in self.GENRES:
            raise ValueError("Not a genre")
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

        #  Validate that genre is in GENRES, raise ValueError if not


    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "available": self.available
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["genre"],
            data["available"]
        )

    def __str__(self) -> str:
        status = "available" if self.available else "Not available"
        return f"[{self.book_id}] {self.tite} by {self.author} ({self.genre}) - {status}"


# =============================================================================
# PART 3: BORROWER CLASS
# =============================================================================

class Borrower:
    """
    Represents a library member who can borrow books.

    Instance Attributes:
        borrower_id (str): Unique identifier
        name (str): Borrower's name
        email (str): Borrower's email
        borrowed_books (list): List of book_ids currently borrowed

    Methods:
        borrow_book(book_id): Add book to borrowed list
        return_book(book_id): Remove book from borrowed list
        to_dict(): Convert to dictionary
        from_dict(data): Class method to create Borrower from dictionary
    """

    MAX_BOOKS = 3  # Maximum books a borrower can have at once

    def __init__(self, borrower_id: str, name: str, email: str, borrowed_books: list = None):
        # Initialize attributes (use empty list if borrowed_books is None)
        self.borrower_id = borrower_id
        self.name = name
        self.email = email
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def can_borrow(self) -> bool:
        """Check if borrower can borrow more books."""
        return len(self.borrowed_books) < self.MAX_BOOKS

    def borrow_book(self, book_id: str) -> bool:
        """Add book to borrowed list. Return False if at max limit."""
        if not self.can_borrow():
            return False
        self.borrowed_books.append(book_id)
        return True

    def return_book(self, book_id: str) -> bool:
        """Remove book from borrowed list. Return False if not found."""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False

    def to_dict(self) -> dict:
        #  Return dictionary with all attributes
        return {
            "borrower_id": self.borrower_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        #  Create and return a Borrower instance from dictionary
        return cls(
            data["borrower_id"],
            data["name"],
            data["email"],
            data["borrowed_books"]
        )


# =============================================================================
# PART 4: LIBRARY CLASS (Main System)
# =============================================================================

class Library:
    """
    Main library system that manages books and borrowers.
    Persists data to JSON files.

    Attributes:
        name (str): Library name
        books (dict): book_id -> Book
        borrowers (dict): borrower_id -> Borrower
        books_file (str): Path to books JSON file
        borrowers_file (str): Path to borrowers JSON file

    Methods:
        add_book(title, author, genre) -> Book: Add a new book
        add_borrower(name, email) -> Borrower: Add a new borrower
        checkout_book(book_id, borrower_id) -> bool: Borrower checks out a book
        return_book(book_id, borrower_id) -> bool: Borrower returns a book
        search_books(**criteria) -> list: Search books by criteria
        get_available_books() -> list: Get all available books
        get_borrower_books(borrower_id) -> list: Get books borrowed by a borrower
        save(): Save all data to JSON files
        load(): Load data from JSON files
    """

    def __init__(self, name: str, data_dir: str = "."):
        self.name = name
        self.books = {}
        self.borrowers = {}
        self.books_file = os.path.join(data_dir, "library_books.json")
        self.borrowers_file = os.path.join(data_dir, "library_borrowers.json")
        self.load()

    def load(self) -> None:
        """Load books and borrowers from JSON files."""
        # TODO: Load books from self.books_file
        # TODO: Load borrowers from self.borrowers_file
        # Hint: Use try/except to handle files not existing
        pass

    def save(self) -> None:
        """Save books and borrowers to JSON files."""
        # TODO: Save self.books to self.books_file
        # TODO: Save self.borrowers to self.borrowers_file
        # Hint: Convert Book/Borrower objects to dicts using to_dict()
        pass

    def add_book(self, title: str, author: str, genre: str) -> Book:
        """Add a new book to the library."""
        #  Generate new book_id using generate_id
        new_id = generate_id("BOOK", list(self.books.keys()))
        book = Book(new_id, title, author, genre)
        self.books[new_id] = book
        self.save()
        return book


    def add_borrower(self, name: str, email: str) -> Borrower:
        """Register a new borrower."""
        # Generate new borrower_id, create Borrower, add to self.borrowers, save, return
        new_id = generate_id("USER", list(self.borrowers.keys()))
        borrower = Borrower(new_id, name, email)
        self.borrowers[new_id] = borrower
        self.save()
        return borrower

    def checkout_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower checks out a book.
        Returns False if book unavailable, borrower not found, or at max limit.
        """
        #  Validate book exists and is available
        if book_id not in self.books:
            return False
        book = self.books[book_id]
        borrower = self.borrowers[borrower_id]
        # Validate borrower exists and can borrow
        if not book.available or not borrower.can_borrow():
            return False
        # Update book.available, borrower.borrowed_books
        book.available = False
        borrower.can_borrow()
        borrower.borrow_book(book_id)
        self.save()
        return True
        #  Save and return True


    def return_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower returns a book.
        Returns False if book/borrower not found or book wasn't borrowed by this person.
        """
        # TODO: Validate book and borrower exist
        # TODO: Validate book is in borrower's borrowed_books
        # TODO: Update book.available, remove from borrowed_books
        # TODO: Save and return True
        pass

    def search_books(self, **criteria) -> list:
        """Search books by any criteria (title, author, genre, available)."""
        #  Use search_items helper function
        # Hint: Convert self.books.values() to list of dicts first
        books_list = [b.to_dict() for b in self.books.values()]
        results = search_items(books_list, **criteria)
        return [Book.from_dict(r) for r in results]

    def get_available_books(self) -> list:
        """Get list of all available books."""
        #  Return books where available=True
        return [b for b in self.books.values() if b.available]

    def get_borrower_books(self, borrower_id: str) -> list:
        """Get list of books currently borrowed by a borrower."""
        # TODO: Get borrower, return list of Book objects for their borrowed_books
        pass

    def get_statistics(self) -> dict:
        """
        Return library statistics.
        Uses the concepts of dict comprehension and aggregation.
        """
        # TODO: Return dict with:
        # - total_books: total number of books
        # - available_books: number of available books
        # - checked_out: number of checked out books
        # - total_borrowers: number of borrowers
        # - books_by_genre: dict of genre -> count
        pass



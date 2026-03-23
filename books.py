#!/usr/bin/env python3
"""
Book List Manager
Manage a list of books with add, remove, search, update, and display operations.
"""


class Book:
    """Represents a single book entry."""

    def __init__(self, title, author, year, genre=""):
        self.title = title
        self.author = author
        self.year = int(year)
        self.genre = genre

    def __str__(self):
        genre_str = f", {self.genre}" if self.genre else ""
        return f'"{self.title}" by {self.author} ({self.year}{genre_str})'


class BookManager:
    """Manages a collection of books."""

    def __init__(self):
        self._books = []

    # ------------------------------------------------------------------ #
    # Core operations
    # ------------------------------------------------------------------ #

    def add_book(self, title, author, year, genre=""):
        """Add a new book to the list."""
        book = Book(title, author, year, genre)
        self._books.append(book)
        return book

    def remove_book(self, title):
        """Remove a book by title (case-insensitive). Returns True if removed."""
        for book in self._books:
            if book.title.lower() == title.lower():
                self._books.remove(book)
                return True
        return False

    def update_book(self, title, author=None, year=None, genre=None):
        """Update an existing book's fields by title (case-insensitive)."""
        book = self.find_by_title(title)
        if book is None:
            return None
        if author is not None:
            book.author = author
        if year is not None:
            book.year = int(year)
        if genre is not None:
            book.genre = genre
        return book

    def list_books(self):
        """Return all books."""
        return list(self._books)

    # ------------------------------------------------------------------ #
    # Search helpers
    # ------------------------------------------------------------------ #

    def find_by_title(self, title):
        """Find a book by exact title match (case-insensitive)."""
        for book in self._books:
            if book.title.lower() == title.lower():
                return book
        return None

    def search(self, query):
        """Search books by title, author, or genre (case-insensitive)."""
        query_lower = query.lower()
        return [
            b for b in self._books
            if query_lower in b.title.lower()
            or query_lower in b.author.lower()
            or query_lower in b.genre.lower()
        ]

    def __len__(self):
        return len(self._books)


# ---------------------------------------------------------------------- #
# CLI helpers
# ---------------------------------------------------------------------- #

def _print_books(books):
    if not books:
        print("  (no books found)")
        return
    for i, book in enumerate(books, 1):
        print(f"  {i}. {book}")


def _prompt(label, required=True):
    while True:
        value = input(f"  {label}: ").strip()
        if value or not required:
            return value
        print("  This field is required.")


def run_cli():
    """Interactive command-line interface for the Book Manager."""
    manager = BookManager()

    MENU = """
========================================
         Book List Manager
========================================
  1. Add a book
  2. Remove a book
  3. List all books
  4. Search books
  5. Update a book
  6. Exit
========================================"""

    while True:
        print(MENU)
        choice = input("Select option (1-6): ").strip()

        if choice == "1":
            print("\n-- Add a Book --")
            title = _prompt("Title")
            author = _prompt("Author")
            year = _prompt("Year")
            genre = _prompt("Genre (optional)", required=False)
            try:
                book = manager.add_book(title, author, year, genre)
                print(f"\nAdded: {book}")
            except ValueError:
                print("\nError: Year must be a number.")

        elif choice == "2":
            print("\n-- Remove a Book --")
            title = _prompt("Title to remove")
            if manager.remove_book(title):
                print(f'\nRemoved: "{title}"')
            else:
                print(f'\nNot found: "{title}"')

        elif choice == "3":
            print(f"\n-- All Books ({len(manager)}) --")
            _print_books(manager.list_books())

        elif choice == "4":
            print("\n-- Search Books --")
            query = _prompt("Search (title / author / genre)")
            results = manager.search(query)
            print(f"\nFound {len(results)} result(s):")
            _print_books(results)

        elif choice == "5":
            print("\n-- Update a Book --")
            title = _prompt("Title of book to update")
            book = manager.find_by_title(title)
            if book is None:
                print(f'\nNot found: "{title}"')
            else:
                print(f"  Current: {book}")
                print("  (Leave blank to keep current value)")
                new_author = _prompt(f"Author [{book.author}]", required=False)
                new_year = _prompt(f"Year [{book.year}]", required=False)
                new_genre = _prompt(f"Genre [{book.genre}]", required=False)
                try:
                    updated = manager.update_book(
                        title,
                        author=new_author or None,
                        year=new_year or None,
                        genre=new_genre or None,
                    )
                    print(f"\nUpdated: {updated}")
                except ValueError:
                    print("\nError: Year must be a number.")

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


if __name__ == "__main__":
    run_cli()

from library_api.models import Book
from library_api.lib.serializers.book_serializer import BookSerializer


def get_all_books():
    """Retrieve all books"""
    return Book.objects.all()


def create_book(book_data):
    """Create a new book"""
    serializer = BookSerializer(data=book_data)
    if serializer.is_valid():
        return serializer.save()
    return None


def get_book(book_id):
    """Retrieve a single book"""
    return Book.objects.filter(id=book_id).first()


def update_book(book_id, book_data):
    """Update the detail/s of a book"""
    book = get_book(book_id)
    if not book:
        return None
    serializer = BookSerializer(book, data=book_data, partial=True)
    if serializer.is_valid():
        return serializer.save()
    return None


def delete_book(book_id):
    """Delete an existing book"""
    book = get_book(book_id)
    if not book:
        return None
    book.delete()
    return True

from library_api.models import Review, Book
from library_api.lib.serializers.review_serializer import ReviewSerializer


def get_reviews(book_id):
    """Retrieve all reviews for a book"""
    return Review.objects.filter(book_id=book_id)


def create_review(user, book_id, review_data):
    """Create a new review for a given book"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None
    review = Review(user=user, book=book)
    serializer = ReviewSerializer(review, data=review_data)
    if serializer.is_valid():
        return serializer.save()
    return None

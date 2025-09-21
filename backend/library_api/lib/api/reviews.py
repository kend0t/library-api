from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from library_api.lib.services.review_services import create_review, get_reviews
from library_api.lib.serializers.review_serializer import ReviewSerializer


class BookReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        """List all reviews for a given book"""
        reviews = get_reviews(book_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, book_id):
        """Add a review to a book"""
        user = request.user
        review = create_review(user, book_id, request.data)

        if not review:
            return Response({"message": "Data provided is invalid or book not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

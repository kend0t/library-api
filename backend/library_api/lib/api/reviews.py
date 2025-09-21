from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from library_api.lib.services.review_services import create_review, get_reviews
from library_api.lib.serializers.review_serializer import ReviewSerializer
from library_api.models import Book
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BookReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all reviews for a given book",
        manual_parameters=[
            openapi.Parameter(
                "book_id",
                openapi.IN_PATH,
                description="Unique ID of the book to get reviews for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: ReviewSerializer(many=True),
            404: "Book not found"
        }
    )
    def get(self, request, book_id):
        """List all reviews for a given book"""
        try:
            Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"message": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        reviews = get_reviews(book_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add a new review for a given book",
        manual_parameters=[
            openapi.Parameter(
                "book_id",
                openapi.IN_PATH,
                description="Unique ID of the book to add a review for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: "Invalid data provided",
            404: "Book not found"
        }
    )
    def post(self, request, book_id):
        """Add a review to a book"""
        user = request.user

        try:
            Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"message": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        review = create_review(user, book_id, request.data)
        if not review:
            return Response(
                {"message": "Data provided is invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

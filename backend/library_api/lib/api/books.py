from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from library_api.lib.services.book_services import get_all_books, create_book, get_book, update_book, delete_book
from library_api.lib.serializers.book_serializer import BookSerializer
from library_api.models import Book
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all books",
        responses={
            200: BookSerializer(many=True)
        }
    )
    def get(self, request):
        """Endpoint for retrieving all books"""
        books = get_all_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=BookSerializer,
        responses={
            201: BookSerializer,
            400: "Invalid or incomplete data"
        }
    )
    def post(self, request):
        """Endpoint for creating a new book"""
        book = create_book(request.data)
        if not book:
            return Response({"message": "Data provided is invalid or incomplete"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookSingleView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve one book by ID",
        manual_parameters=[
            openapi.Parameter(
                "book_id",
                openapi.IN_PATH,
                description="Unique ID of the book to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: BookSerializer,
            404: "Book not found"
        }

    )
    def get(self, request, book_id):
        """Endpoint for retrieving a single book"""
        book = get_book(book_id)
        if not book:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update an existing book by ID",
        manual_parameters=[
            openapi.Parameter(
                "book_id",
                openapi.IN_PATH,
                description="Unique ID of the book to update",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=BookSerializer,
        responses={
            200: BookSerializer,
            400: "Invalid input data",
            404: "Book not found"
        }
    )
    def patch(self, request, book_id):
        """Endpoint for updating an existing book"""
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({
                "message": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)

        book = update_book(book_id, request.data)
        if not book:
            return Response({"message": "Data provided is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a book by ID",
        manual_parameters=[
            openapi.Parameter(
                "book_id",
                openapi.IN_PATH,
                description="Unique ID of the book to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            204: "Book successfully deleted",
            400: "Book not found"
        }
    )
    def delete(self, request, book_id):
        """Endpoint for deleting a book"""
        deleted_book = delete_book(book_id)
        if not deleted_book:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Book succesfully deleted"}, status=status.HTTP_204_NO_CONTENT)

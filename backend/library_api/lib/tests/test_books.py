import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from library_api.models import Book, User


@pytest.mark.django_db
class TestBookAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.book = Book.objects.create(
            title="Test Case Book", author="Tester", published_date="2025-09-21")
        self.book_list_url = reverse("all-books")
        self.book_single_url = reverse("single-book", args=[self.book.id])
        self.client.force_authenticate(user=self.user)

    def test_get_books(self):
        """Test case for retrieving all books"""
        Book.objects.create(
            title="Existing book",
            author="Some author",
            published_date="2025-09-21"
        )
        response = self.client.get(self.book_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_book(self):
        """Test case for creating a book"""
        data = {
            "title": "Test Book",
            "author": "Tester",
            "published_date": "2025-09-21"
        }
        response = self.client.post(self.book_list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Test Book"

    def test_create_invalid_book(self):
        """Test case for creating an invalid book"""
        data = {"title": ""}
        response = self.client.post(self.book_list_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Data provided is invalid or incomplete"

    def test_get_single_book(self):
        """Test case for retrieving a single book"""
        response = self.client.get(self.book_single_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Case Book"
        assert response.data["author"] == "Tester"

    def test_get_nonexistent_book(self):
        """Test case for retrieving a non-existent book"""
        url = reverse("single-book", args=[99999])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_book(self):
        """Test case for updating an existing book"""
        data = {"title": "Updated Book Title"}
        response = self.client.patch(self.book_single_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Book Title"

    def test_update_nonexistent_book(self):
        """Test case for updating a non-existent book"""
        url = reverse("single-book", args=[99999])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_book(self):
        """Test case for deleting an existing book"""
        response = self.client.delete(self.book_single_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_nonexistent_book(self):
        """Test case for deleting a non-existent book"""
        url = reverse("single-book", args=[99999])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

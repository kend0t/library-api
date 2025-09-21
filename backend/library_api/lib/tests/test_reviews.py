import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from library_api.models import Book, Review, User


@pytest.mark.django_db
class TestReviewAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reviewuser", password="password123")
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Book for Review",
            author="Reviewer Author",
            published_date="2025-09-21"
        )
        self.reviews_url = reverse(
            "reviews", args=[self.book.id])

    def test_create_review(self):
        """Test case for creating a review"""
        data = {
            "rating": 5,
            "comment": "Excellent book!"
        }
        response = self.client.post(self.reviews_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["comment"] == "Excellent book!"
        assert response.data["rating"] == 5

    def test_invalid_review(self):
        """Test case for invalid review creation"""
        data = {"rating": 10, "comment": ""}
        response = self.client.post(self.reviews_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_reviews(self):
        """Test case for listing reviews of a book"""
        Review.objects.create(
            user=self.user,
            book=self.book,
            rating=4,
            comment="Nice book!"
        )
        response = self.client.get(self.reviews_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_list_reviews_invalid_book(self):
        """Test case for listing reviews with invalid book ID"""
        wrong_url = reverse("reviews", args=[9999])
        response = self.client.get(wrong_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Book not found"

    def test_create_review_invalid_book(self):
        """Test case for creating a review with invalid book ID"""
        wrong_url = reverse("reviews", args=[9999])
        data = {
            "rating": 4,
            "comment": "Test"
        }
        response = self.client.post(wrong_url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Book not found"

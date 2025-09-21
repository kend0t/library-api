import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from library_api.models import User
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_register_user(self):
        """Test case for registering a new user"""
        data = {
            "username": "testuser",
            "password": "testuser"
        }
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "testuser"

    def test_register_taken_user(self):
        """Test case for registering an already taken username"""
        User.objects.create(username="takenuser", password="password")
        data = {
            "username": "takenuser",
            "password": "password"
        }
        response = self.client.post(self.register_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "This username is already taken."

    def test_login(self):
        """Test case for logging in with JWT"""
        User.objects.create_user(username="testuser", password="password")
        data = {
            "username": "testuser",
            "password": "password"
        }
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_login(self):
        """Test that login fails with wrong username or password"""
        data = {
            "username": "wronguser",
            "password": "wrongpass"
        }
        response = self.client.post(self.login_url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "no_active_account" in str(response.data)

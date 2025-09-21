from rest_framework import serializers
from library_api.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "username", "book_title",
                  "rating", "comment", "created_at"]

from django.urls import path
from library_api.lib.api.books import BookListView, BookSingleView
from library_api.lib.api.reviews import BookReviewView

urlpatterns = [
    path('books/', BookListView.as_view(), name="all-books"),  # GET (all), POST
    path('books/<int:book_id>', BookSingleView.as_view(),
         name="single-book"),  # GET (with id), PATCH, DELETE
    path('books/<int:book_id>/reviews/', BookReviewView.as_view(),
         name="reviews")
]

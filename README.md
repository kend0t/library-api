# Library API
A simple Django REST Framework API with JWT authentication for managing books and reviews.

---

## Setup
1. Clone the repository and navigate to the backend folder.
2. Create a virtual environment
3. Install the dependencies via `pip install -r requirements.txt`
4. Run migrations via `python manage.py migrate`
5. Start the development server via `python manage.py runserver`
6. Access the API docs using `http://127.0.0.1:8000/swagger/`

## Endpoints
### Auth
- **POST** `/api/auth/register/` -> Register a new user
- **POST** `/api/auth/login/` -> Login and get JWT tokens
- Use the `access` token in your Auth headers to use the books and reviews endpoints
- 
### Books
- **GET** `/api/books/` -> List all books
- **POST** `/api/books/` -> Create a new book
- **GET** `/api/books/{book_id}/` -> Retrieve a book
- **PATCH** `/api/books/{book_id}/` -> Update a book
- **DELETE** `/api/books/{book_id}/` -> Delete a book

### Reviews
- **GET** `/api/books/{book_id}/reviews/` -> List reviews for a book
- **POST** `/api/books/{book_id}/reviews/` -> Add a review to a book

### Docs
- **GET** `/swagger/` -> Swagger UI (API Documentation)

**Note**: All endpoints (except register/login) require JWT authentication `(Authorization: Bearer <access_token>)`




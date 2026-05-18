from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.constants import NUM_OF_ITEMS_PER_PAGE
from book.factories import AuthorFactory, BookFactory
from book.models import Book
from book.serializers import AuthorSerializer
from reference_values.factories import GenreFactory, LanguageFactory
from reference_values.serializers import GenreSerializer, LanguageSerializer
from user import constants
from user.factories import UserFactory

CREATE_BOOK_URL = reverse("book:create_book")
LIST_BOOK_URL = reverse("book:list_book")


class PublicBookApiTests(TestCase):
    """Test book API (public)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()

    def test_create_book_unauthenticated_fails(self):
        """Test creating a book by an unauthenticated user"""

        author = AuthorFactory()
        language = LanguageFactory()
        genre = GenreFactory()

        payload = {
            "title": "Test book",
            "author": [author.id],
            "isbn": "111",
            "language": [language.id],
            "genre": [genre.id],
        }

        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_unauthenticated_fails(self):
        """Test retrieving a book by an unauthenticated user"""
        book = BookFactory()
        res = self.client.get(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthenticated_fails(self):
        """Test deleting a book by an unauthenticated user"""
        book = BookFactory()
        res = self.client.delete(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthenticated_fails(self):
        """Test updating a book by an unauthenticated user"""
        first_book, second_book = BookFactory.create_batch(2)

        author_ids = [author.id for author in second_book.author.all()]
        language_ids = [language.id for language in second_book.language.all()]
        genre_ids = [genre.id for genre in second_book.genre.all()]

        payload = {
            "id": first_book.id,
            "title": "Updated title",
            "author": author_ids,
            "published_date": "2000-01-01",
            "isbn": "Updated isbn",
            "pages": 10,
            "cover": "http://www.test.com/test.jpg",
            "language": language_ids,
            "genre": genre_ids,
        }

        res = self.client.put(reverse("book:manage_book", kwargs={"pk": first_book.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books_unauthenticated_fails(self):
        """Test listing books by an unauthenticated user"""
        BookFactory.create_batch(2)
        res = self.client.get(LIST_BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiUserAdminTests(TestCase):
    """Test book API for an authenticated admin user (private)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

        self.maxDiff = None

    def test_create_book_success(self):
        """Test creating a book by an authenticated user in admin group"""

        author = AuthorFactory()
        language = LanguageFactory()
        genre = GenreFactory()

        payload = {
            "title": "Test book",
            "author": [author.id],
            "isbn": "111",
            "language": [language.id],
            "genre": [genre.id],
        }

        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        books = Book.objects.all()
        self.assertEqual(books.count(), 1)

        book = books.first()
        expected_data = {
            "id": book.id,
            "title": book.title,
            "author": AuthorSerializer(book.author, many=True).data,
            "published_date": str(book.published_date) if book.published_date else None,
            "isbn": book.isbn,
            "pages": book.pages,
            "cover": book.cover,
            "language": LanguageSerializer(book.language, many=True).data,
            "genre": GenreSerializer(book.genre, many=True).data,
        }
        self.assertEqual(res.json(), expected_data)

    def test_retrieve_book_success(self):
        """Test retrieving a book by an authenticated user in admin group"""
        book = BookFactory()
        expected_data = {
            "id": book.id,
            "title": book.title,
            "author": AuthorSerializer(book.author, many=True).data,
            "published_date": str(book.published_date),
            "isbn": book.isbn,
            "pages": book.pages,
            "cover": book.cover,
            "language": LanguageSerializer(book.language, many=True).data,
            "genre": GenreSerializer(book.genre, many=True).data,
        }
        res = self.client.get(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_delete_book_success(self):
        """Test deleting a book by an authenticated user in admin group"""
        book = BookFactory()
        res = self.client.delete(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(id=book.id).first(), None)

    def test_partial_update_book_success(self):
        """Test partially updating a book by an authenticated user in admin group"""
        book = BookFactory.create()
        updated_title = "Updated title"
        payload = {
            "title": updated_title,
        }
        expected_data = {
            "id": book.id,
            "title": updated_title,
            "author": AuthorSerializer(book.author, many=True).data,
            "published_date": book.published_date,
            "isbn": book.isbn,
            "pages": book.pages,
            "cover": book.cover,
            "language": LanguageSerializer(book.language, many=True).data,
            "genre": GenreSerializer(book.genre, many=True).data,
        }

        res = self.client.patch(reverse("book:manage_book", kwargs={"pk": book.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_full_update_book_success(self):
        """Test partially updating a book by an authenticated user in admin group"""
        first_book, second_book = BookFactory.create_batch(2)

        author_ids = [author.id for author in second_book.author.all()]
        language_ids = [language.id for language in second_book.language.all()]
        genre_ids = [genre.id for genre in second_book.genre.all()]

        payload = {
            "id": first_book.id,
            "title": "Updated title",
            "author": author_ids,
            "published_date": "2000-01-01",
            "isbn": "Updated isbn",
            "pages": 10,
            "cover": "http://www.test.com/test.jpg",
            "language": language_ids,
            "genre": genre_ids,
        }

        expected_data = {
            "id": first_book.id,
            "title": "Updated title",
            "author": AuthorSerializer(second_book.author, many=True).data,
            "published_date": "2000-01-01",
            "isbn": "Updated isbn",
            "pages": 10,
            "cover": "http://www.test.com/test.jpg",
            "language": LanguageSerializer(second_book.language, many=True).data,
            "genre": GenreSerializer(second_book.genre, many=True).data,
        }

        res = self.client.put(reverse("book:manage_book", kwargs={"pk": first_book.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_list_books_paginated_by_user_admin_success(self):
        """Test listing paginated books by an authenticated user in admin group"""
        BookFactory.create_batch(NUM_OF_ITEMS_PER_PAGE + 1)
        res = self.client.get(LIST_BOOK_URL, {"page": 2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)

    def test_list_books_filtered_success(self):
        """Test listing filtered books by author, published_date and language by an authenticated user in admin group"""
        author1 = AuthorFactory(last_name="foo")
        author2 = AuthorFactory(last_name="bar")
        author3 = AuthorFactory(last_name="baz")
        language1 = LanguageFactory(name="English")
        language2 = LanguageFactory(name="German", two_letter_code="de", three_letter_code="deu")
        language3 = LanguageFactory(name="French", three_letter_code="fra")
        BookFactory.create(title="qux", author=[author1], published_date="1980-01-01", language=[language1])
        BookFactory.create(title="corge", author=[author2], published_date="1990-01-01", language=[language2])
        BookFactory.create(title="grault", author=[author3], published_date="2000-01-01", language=[language3])

        res = self.client.get(LIST_BOOK_URL, {"title": "qux"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)
        self.assertEqual(res.json().get("results")[0].get("title"), "qux")

        res = self.client.get(LIST_BOOK_URL, {"author": "foo"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)
        self.assertEqual(res.json().get("results")[0].get("author")[0].get("last_name"), "foo")

        res = self.client.get(LIST_BOOK_URL, {"publication_year": 1990})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)
        self.assertEqual(res.json().get("results")[0].get("published_date"), "1990-01-01")

        res = self.client.get(LIST_BOOK_URL, {"language": "fr"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)
        self.assertEqual(res.json().get("results")[0].get("language")[0].get("two_letter_code"), "fr")


class PrivateBookApiUserNotAdminTests(TestCase):
    """Test book API for an authenticated user not admin (private)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

        self.maxDiff = None

    def test_create_book_by_user_not_admin_fails(self):
        """Test creating a book by an authenticated user not in admin group"""

        author = AuthorFactory()
        language = LanguageFactory()
        genre = GenreFactory()

        payload = {
            "title": "Test book",
            "author": [author.id],
            "isbn": "111",
            "language": [language.id],
            "genre": [genre.id],
        }

        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_by_user_not_admin_success(self):
        """Test retrieving a book by an authenticated user not in admin group"""
        book = BookFactory()
        expected_data = {
            "id": book.id,
            "title": book.title,
            "author": AuthorSerializer(book.author, many=True).data,
            "published_date": str(book.published_date),
            "isbn": book.isbn,
            "pages": book.pages,
            "cover": book.cover,
            "language": LanguageSerializer(book.language, many=True).data,
            "genre": GenreSerializer(book.genre, many=True).data,
        }
        res = self.client.get(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.json(), expected_data)

    def test_delete_book_by_user_not_admin_fails(self):
        """Test deleting a book by an authenticated user not in admin group"""
        book = BookFactory()
        res = self.client.delete(reverse("book:manage_book", kwargs={"pk": book.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_by_user_not_admin_fails(self):
        """Test partially updating a book by an authenticated user not in admin group"""
        first_book, second_book = BookFactory.create_batch(2)

        author_ids = [author.id for author in second_book.author.all()]
        language_ids = [language.id for language in second_book.language.all()]
        genre_ids = [genre.id for genre in second_book.genre.all()]

        payload = {
            "id": first_book.id,
            "title": "Updated title",
            "author": author_ids,
            "published_date": "2000-01-01",
            "isbn": "Updated isbn",
            "pages": 10,
            "cover": "http://www.test.com/test.jpg",
            "language": language_ids,
            "genre": genre_ids,
        }

        res = self.client.put(reverse("book:manage_book", kwargs={"pk": first_book.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_books_paginated_by_user_admin_success(self):
        """Test listing paginated books by an authenticated user not in admin group"""
        BookFactory.create_batch(NUM_OF_ITEMS_PER_PAGE + 1)
        res = self.client.get(LIST_BOOK_URL, {"page": 2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get("results")), 1)

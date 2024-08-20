from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.constants import NUM_OF_ITEMS_PER_PAGE
from book.factories import BookFactory
from book.models import Book
from user import factories

CREATE_BOOK_URL = reverse('book:create_book')
LIST_BOOK_URL = reverse('book:list_book')


class PublicBookApiTests(TestCase):
    """Test book API (public)"""

    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.client = APIClient()

    def test_create_book_unauthenticated_fail(self):
        """Test creating a book with an unauthenticated user"""

        payload = {
            'title': 'Test book',
            'author': 'Test author',
            'isbn': '111',
            'language': 'Test'
        }

        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_unauthenticated_fail(self):
        """Test retrieving a book with an unauthenticated user"""
        BookFactory.create()
        book_id = Book.objects.first().id
        res = self.client.get(reverse('book:manage_book', kwargs={'pk': book_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthenticated_fail(self):
        """Test deleting a book with an unauthenticated user"""
        BookFactory.create()
        book_id = Book.objects.first().id
        res = self.client.delete(reverse('book:manage_book', kwargs={'pk': book_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthenticated_fail(self):
        """Test updating a book with an unauthenticated user"""
        BookFactory.create()
        book_id = Book.objects.first().id

        payload = {
            'title': 'Test book',
            'author': 'Test author',
            'isbn': '111',
            'language': 'Test'
        }

        res = self.client.put(reverse('book:manage_book', kwargs={'pk': book_id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books_unauthenticated_fail(self):
        """Test listing books with an unauthenticated user"""
        BookFactory.create_batch(2)
        res = self.client.get(LIST_BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):
    """Test book API (private)"""

    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_book_success(self):
        """Test creating a book with an authenticated user"""

        payload = {
            'title': 'Test book',
            'author': 'Test author',
            'isbn': '111',
            'language': 'Test'
        }

        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        books = Book.objects.all()
        self.assertEqual(books.count(), 1)

        book = books.first()
        expected_data = {
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'language': book.language
        }
        self.assertEqual(expected_data, payload)

    def test_retrieve_book_success(self):
        """Test retrieving a book with an authenticated user"""
        BookFactory.create()
        book = Book.objects.first()
        expected_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': str(book.published_date),
            'isbn': book.isbn,
            'pages': book.pages,
            'cover': book.cover,
            'language': book.language
        }
        res = self.client.get(reverse('book:manage_book', kwargs={'pk': book.id}))
        self.assertEqual(res.json(), expected_data)

    def test_delete_book_success(self):
        """Test deleting a book with an authenticated user"""
        BookFactory.create()
        book_id = Book.objects.first().id
        res = self.client.delete(reverse('book:manage_book', kwargs={'pk': book_id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(id=book_id).first(), None)

    def test_partial_update_book_success(self):
        """Test partially updating a book with an authenticated user"""
        BookFactory.create()
        book = Book.objects.first()
        updated_title = 'Updated title'
        payload = {
            'title': updated_title,
        }
        expected_data = {
            'id': book.id,
            'title': updated_title,
            'author': book.author,
            'published_date': str(book.published_date),
            'isbn': book.isbn,
            'pages': book.pages,
            'cover': book.cover,
            'language': book.language
        }

        res = self.client.patch(reverse('book:manage_book', kwargs={'pk': book.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), expected_data)

    def test_full_update_book_success(self):
        """Test partially updating a book with an authenticated user"""
        BookFactory.create()
        book_id = Book.objects.first().id

        payload = {
            'id': book_id,
            'title': 'Updated title',
            'author': 'Updated author',
            'published_date': '2000-01-01',
            'isbn': 'Updated isbn',
            'pages': 10,
            'cover': 'http://www.test.com/test.jpg',
            'language': 'Updated langauge'
        }

        res = self.client.patch(reverse('book:manage_book', kwargs={'pk': book_id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), payload)

    def test_list_books_paginated_success(self):
        """Test listing paginated books with an authenticated user"""
        BookFactory.create_batch(NUM_OF_ITEMS_PER_PAGE + 1)
        res = self.client.get(LIST_BOOK_URL, {'page': 2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get('results')), 1)

    def test_list_books_filtered_success(self):
        """Test listing paginated books with an authenticated user"""
        BookFactory.create(language='En')
        BookFactory.create(language='De')
        BookFactory.create(language='Fr')
        res = self.client.get(LIST_BOOK_URL, {'language': 'Fr'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json().get('results')), 1)
        self.assertEqual(res.json().get('results')[0].get('language'), 'Fr')

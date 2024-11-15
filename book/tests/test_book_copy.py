from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.factories import AuthorFactory, BookFactory, BookCopyFactory
from book.models import Author, BookCopy
from reference_values.models import Language
from user import factories, constants

CREATE_BOOK_COPY_URL = reverse('book:create_book_copy')
LIST_BOOK_COPY_URL = reverse('book:list_book_copy')

class PublicBookCopyApiTest(TestCase):
    """Test book copy API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()

    def test_create_book_copy_by_unauthenticated_user_fails(self):
        """Test creating a book copy by an unauthenticated user"""

        book = BookFactory()

        payload = {
            'book_id': book.id,
        }

        res = self.client.post(CREATE_BOOK_COPY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_copy_by_unauthenticated_user_fails(self):
        """Test retrieving a book copy by an unauthenticated user"""
        book_copy = BookCopyFactory.create()
        res = self.client.get(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_copy_by_unauthenticated_user_fails(self):
        """Test deleting a book copy by an unauthenticated user"""
        book_copy = BookCopyFactory.create()
        res = self.client.delete(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_book_copies_by_unauthenticated_user_fails(self):
        """Test getting list of book copies by an unauthenticated user"""
        BookCopyFactory.create_batch(2)
        res = self.client.get(LIST_BOOK_COPY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookCopyApiUserNotAdminTest(TestCase):
    """Test book copy API for an authenticated not admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_book_copy_by_user_not_admin_fails(self):
        """Test creating a book copy by an authenticated user not in admin group"""

        book = BookFactory()

        payload = {
            'book_id': book.id,
        }

        res = self.client.post(CREATE_BOOK_COPY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_copy_by_user_not_admin_success(self):
        """Test retrieving a book copy by an authenticated user not in admin group"""
        book_copy = BookCopyFactory.create()
        res = self.client.get(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book_copy_by_user_not_admin_fails(self):
        """Test deleting a book copy by an authenticated user not in admin group"""
        book_copy = BookCopyFactory.create()
        res = self.client.delete(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_author_by_user_not_admin_fails(self):
        """Test getting list of book copies by an authenticated user not in admin group"""
        BookCopyFactory.create_batch(2)
        res = self.client.get(LIST_BOOK_COPY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateAuthorApiUserAdminTest(TestCase):
    """Test author API for an authenticated admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_book_copy_by_user_admin_success(self):
        """Test creating a book copy by an authenticated user in admin group"""

        book = BookFactory()

        payload = {
            'book_id': book.id,
        }

        res = self.client.post(CREATE_BOOK_COPY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_book_copy_by_user_admin_success(self):
        """Test retrieving a book copy by an authenticated user in admin group"""
        book_copy = BookCopyFactory.create()
        res = self.client.get(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book_copy_by_user_admin_success(self):
        """Test deleting a book copy by an authenticated user in admin group"""
        book_copy = BookCopyFactory.create()
        res = self.client.delete(reverse('book:manage_book_copy', kwargs={'pk': book_copy.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookCopy.objects.filter(id=book_copy.id).first(), None)

    def test_list_book_copy_by_user_admin_success(self):
        """Test getting list of book copy by an authenticated user in admin group"""
        BookCopyFactory.create_batch(2)
        res = self.client.get(LIST_BOOK_COPY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.factories import AuthorFactory
from book.models import Author
from reference_values.models import Language
from user import factories, constants

CREATE_AUTHOR_URL = reverse('book:create_author')
LIST_AUTHOR_URL = reverse('book:list_author')

class PublicAuthorApiTest(TestCase):
    """Test author API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()

    def test_create_author_by_unauthenticated_user_fails(self):
        """Test creating an author by an unauthenticated user"""

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.post(CREATE_AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_author_by_unauthenticated_user_fails(self):
        """Test retrieving an author by an unauthenticated user"""
        author = AuthorFactory.create()
        res = self.client.get(reverse('reference_values:manage_language', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_author_by_unauthenticated_user_fails(self):
        """Test deleting a language by an unauthenticated user"""
        author = AuthorFactory.create()
        res = self.client.delete(reverse('reference_values:manage_language', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_author_by_unauthenticated_user_fails(self):
        """Test updating an author by an unauthenticated user"""
        author = AuthorFactory.create()

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.put(reverse('book:manage_author', kwargs={'pk': author.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authors_by_unauthenticated_user_fails(self):
        """Test getting list of authors by an unauthenticated user"""
        AuthorFactory.create_batch(2)
        res = self.client.get(LIST_AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorApiUserNotAdminTest(TestCase):
    """Test author API for an authenticated not admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_author_by_user_not_admin_fails(self):
        """Test creating an author by an authenticated user not in admin group"""

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.post(CREATE_AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_author_by_user_not_admin_success(self):
        """Test retrieving an author by an authenticated user not in admin group"""
        author = AuthorFactory.create()
        res = self.client.get(reverse('book:manage_author', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_author_by_user_not_admin_fails(self):
        """Test deleting an author by an authenticated user not in admin group"""
        author = AuthorFactory.create()
        res = self.client.delete(reverse('book:manage_author', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author_by_user_not_admin_fails(self):
        """Test updating an author by an authenticated user not in admin group"""
        AuthorFactory.create()
        author = Author.objects.first()

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.put(reverse('reference_values:manage_language', kwargs={'pk': author.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_author_by_user_not_admin_fails(self):
        """Test getting list of authors by an authenticated user not in admin group"""
        AuthorFactory.create_batch(2)
        res = self.client.get(LIST_AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateAuthorApiUserAdminTest(TestCase):
    """Test author API for an authenticated admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_author_by_user_admin_success(self):
        """Test creating an author by an authenticated user in admin group"""

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.post(CREATE_AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_author_by_user_admin_success(self):
        """Test retrieving an author by an authenticated user in admin group"""
        author = AuthorFactory.create()
        res = self.client.get(reverse('book:manage_author', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_author_by_user_admin_success(self):
        """Test deleting an author by an authenticated user in admin group"""
        author = AuthorFactory.create()
        res = self.client.delete(reverse('book:manage_author', kwargs={'pk': author.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.filter(id=author.id).first(), None)

    def test_update_author_by_user_admin_success(self):
        """Test updating an author by an authenticated user in admin group"""
        author = AuthorFactory.create()

        payload = {
            'last_name': 'Test lastname',
            'first_name': 'Test first name',
            'middle_name': 'Test middle name',
        }

        res = self.client.put(reverse('book:manage_author', kwargs={'pk': author.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_author_by_user_admin_success(self):
        """Test getting list of authors by an authenticated user in admin group"""
        AuthorFactory.create_batch(2)
        res = self.client.get(LIST_AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

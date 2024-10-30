from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from reference_values.models import Language
from reference_values.factories import LanguageFactory
from user import factories, constants

ADD_LANGUAGE_URL = reverse('reference_values:add_language')
LIST_LANGUAGE_URL = reverse('reference_values:list_language')

class PublicLanguageApiTest(TestCase):
    """Test language API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()

    def test_create_language_by_unauthenticated_user_fails(self):
        """Test creating a language by an unauthenticated user"""

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.post(ADD_LANGUAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_language_by_unauthenticated_user_fails(self):
        """Test retrieving a language by an unauthenticated user"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.get(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_language_by_unauthenticated_user_fails(self):
        """Test deleting a language by an unauthenticated user"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.delete(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_language_by_unauthenticated_user_fails(self):
        """Test updating a language by an unauthenticated user"""
        LanguageFactory.create()
        language_id = Language.objects.first().id

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.put(reverse('reference_values:manage_language', kwargs={'pk': language_id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_languages_by_unauthenticated_user_fails(self):
        """Test getting list of languages by an unauthenticated user"""
        LanguageFactory.create_batch(2)
        res = self.client.get(LIST_LANGUAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLanguageApiUserNotAdminTest(TestCase):
    """Test language API for not admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_language_by_user_not_admin_fails(self):
        """Test creating a language by a user not in admin group"""

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.post(ADD_LANGUAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_language_by_user_not_admin_success(self):
        """Test retrieving a language by a user not in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.get(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_language_by_user_not_admin_fails(self):
        """Test deleting a language by a user not in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.delete(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_language_by_user_not_admin_fails(self):
        """Test updating a language by a user not in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.put(reverse('reference_values:manage_language', kwargs={'pk': language_id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_languages_by_user_not_admin_fails(self):
        """Test getting list of languages by a user not in admin group"""
        LanguageFactory.create_batch(2)
        res = self.client.get(LIST_LANGUAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateLanguageApiUserAdminTest(TestCase):
    """Test language API for admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_language_by_user_admin_success(self):
        """Test creating a language by a user in admin group"""

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.post(ADD_LANGUAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_language_by_user_admin_success(self):
        """Test retrieving a language by a user in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.get(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_language_by_user_admin_success(self):
        """Test deleting a language by a user in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id
        res = self.client.delete(reverse('reference_values:manage_language', kwargs={'pk': language_id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.filter(id=language_id).first(), None)

    def test_update_language_by_user_admin_success(self):
        """Test updating a language by a user in admin group"""
        LanguageFactory.create()
        language_id = Language.objects.first().id

        payload = {
            'name': 'Test language',
            'two_letter_code': 'ab',
            'three_letter_code': 'abc'
        }

        res = self.client.put(reverse('reference_values:manage_language', kwargs={'pk': language_id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_languages_by_user_admin_success(self):
        """Test getting list of languages by a user in admin group"""
        LanguageFactory.create_batch(2)
        res = self.client.get(LIST_LANGUAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
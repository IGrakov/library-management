from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from reference_values.factories import GenreFactory
from reference_values.models import Genre
from user import constants, factories

ADD_GENRE_URL = reverse("reference_values:add_genre")
LIST_GENRE_URL = reverse("reference_values:list_genre")


class PublicGenreApiTest(TestCase):
    """Test genre API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()

    def test_create_genre_by_unauthenticated_user_fails(self):
        """Test creating a genre by an unauthenticated user"""

        payload = {
            "name": "Test genre",
        }

        res = self.client.post(ADD_GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_genre_by_unauthenticated_user_fails(self):
        """Test retrieving a genre by an unauthenticated user"""
        genre = GenreFactory.create()
        res = self.client.get(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_genre_by_unauthenticated_user_fails(self):
        """Test deleting a genre by an unauthenticated user"""
        genre = GenreFactory.create()
        res = self.client.delete(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_genre_by_unauthenticated_user_fails(self):
        """Test updating a genre by an unauthenticated user"""
        genre = GenreFactory.create()

        payload = {
            "name": "Test genre",
        }

        res = self.client.put(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_genres_by_unauthenticated_user_fails(self):
        """Test getting list of genres by an unauthenticated user"""
        GenreFactory.create_batch(2)
        res = self.client.get(LIST_GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiUserNotAdminTest(TestCase):
    """Test genre API for an authenticated not admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_genre_by_user_not_admin_fails(self):
        """Test creating a genre by an authenticated user not in admin group"""

        payload = {
            "name": "Test genre",
        }

        res = self.client.post(ADD_GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_genre_by_user_not_admin_success(self):
        """Test retrieving a genre by an authenticated user not in admin group"""
        genre = GenreFactory.create()
        res = self.client.get(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_genre_by_user_not_admin_fails(self):
        """Test deleting a genre by an authenticated user not in admin group"""
        genre = GenreFactory.create()
        res = self.client.delete(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_genre_by_user_not_admin_fails(self):
        """Test updating a genre by an authenticated user not in admin group"""
        genre = GenreFactory.create()

        payload = {
            "name": "Test genre",
        }

        res = self.client.put(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_genres_by_user_not_admin_fails(self):
        """Test getting list of genres by an authenticated user not in admin group"""
        GenreFactory.create_batch(2)
        res = self.client.get(LIST_GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateGenreApiUserAdminTest(TestCase):
    """Test genre API for an authenticated admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_genre_by_user_admin_success(self):
        """Test creating a genre by an authenticated user in admin group"""

        payload = {
            "name": "Test genre",
        }

        res = self.client.post(ADD_GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_genre_by_user_admin_success(self):
        """Test retrieving a genre by an authenticated user in admin group"""
        genre = GenreFactory.create()
        res = self.client.get(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_genre_by_user_admin_success(self):
        """Test deleting a genre by an authenticated user in admin group"""
        genre = GenreFactory.create()
        res = self.client.delete(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.filter(id=genre.id).first(), None)

    def test_update_genre_by_user_admin_success(self):
        """Test updating a genre by an authenticated user in admin group"""
        genre = GenreFactory.create()

        payload = {
            "name": "Test genre",
        }

        res = self.client.put(reverse("reference_values:manage_genre", kwargs={"pk": genre.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_genres_by_user_admin_success(self):
        """Test getting list of genres by an authenticated user in admin group"""
        GenreFactory.create_batch(2)
        res = self.client.get(LIST_GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

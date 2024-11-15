from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from reference_values.constants import HallTypes
from reference_values.models import Hall
from reference_values.factories import HallFactory
from user import factories, constants

ADD_HALL_URL = reverse('reference_values:add_hall')
LIST_HALL_URL = reverse('reference_values:list_hall')

class PublicHallApiTest(TestCase):
    """Test hall API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()

    def test_create_hall_by_unauthenticated_user_fails(self):
        """Test creating a hall by an unauthenticated user"""

        payload = {
            'name': HallTypes.READING_HALL,
        }

        res = self.client.post(ADD_HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_hall_by_unauthenticated_user_fails(self):
        """Test retrieving a hall by an unauthenticated user"""
        hall = HallFactory.create()
        res = self.client.get(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_hall_by_unauthenticated_user_fails(self):
        """Test deleting a hall by an unauthenticated user"""
        hall = HallFactory.create()
        res = self.client.delete(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_hall_by_unauthenticated_user_fails(self):
        """Test updating a hall by an unauthenticated user"""
        hall = HallFactory.create()

        payload = {
            'name': 'Test hall',
        }

        res = self.client.put(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_hall_by_unauthenticated_user_fails(self):
        """Test getting list of hall by an unauthenticated user"""
        HallFactory.create_batch(2)
        res = self.client.get(LIST_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHallApiUserNotAdminTest(TestCase):
    """Test hall API for an authenticated not admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        librarian_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        reader_group.user_set.add(self.user.id)
        librarian_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_hall_by_user_not_admin_fails(self):
        """Test creating a hall by an authenticated user not in admin group"""

        payload = {
            'name': HallTypes.READING_HALL,
        }

        res = self.client.post(ADD_HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_hall_by_user_not_admin_success(self):
        """Test retrieving a hall by an authenticated user not in admin group"""
        hall = HallFactory.create()
        res = self.client.get(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_hall_by_user_not_admin_fails(self):
        """Test deleting a hall by an authenticated user not in admin group"""
        hall = HallFactory.create()
        res = self.client.delete(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_hall_by_user_not_admin_fails(self):
        """Test updating a hall by an authenticated user not in admin group"""
        hall = HallFactory.create()

        payload = {
            'name': HallTypes.READING_HALL,
        }

        res = self.client.put(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_halls_by_user_not_admin_fails(self):
        """Test getting list of halls by an authenticated user not in admin group"""
        HallFactory.create_batch(2)
        res = self.client.get(LIST_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateHallApiUserAdminTest(TestCase):
    """Test hall API for an authenticated admin user (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = factories.UserFactory()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

    def test_create_hall_by_user_admin_success(self):
        """Test creating a hall by an authenticated user in admin group"""

        payload = {
            'name': 'Test hall',
        }

        res = self.client.post(ADD_HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_hall_by_user_admin_success(self):
        """Test retrieving a hall by an authenticated user in admin group"""
        hall = HallFactory.create()
        res = self.client.get(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_hall_by_user_admin_success(self):
        """Test deleting a hall by an authenticated user in admin group"""
        hall = HallFactory.create()
        res = self.client.delete(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hall.objects.filter(id=hall.id).first(), None)

    def test_update_hall_by_user_admin_success(self):
        """Test updating a hall by an authenticated user in admin group"""
        hall = HallFactory.create()

        payload = {
            'name': 'Test hall',
        }

        res = self.client.put(reverse('reference_values:manage_hall', kwargs={'pk': hall.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_halls_by_user_admin_success(self):
        """Test getting list of halls by an authenticated user in admin group"""
        HallFactory.create_batch(2)
        res = self.client.get(LIST_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

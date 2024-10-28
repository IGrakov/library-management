from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user import constants
from user.factories import UserFactory

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

TEST_FIRST_NAME = 'Test first name'
TEST_LAST_NAME = 'Test last name'
TEST_EMAIL = 'test@test.com'


class UserRoleByDefaultTests(TestCase):
    """Test assignment of user roles by default"""

    def test_user_is_assigned__at_creation_to_reader_group_by_default(self):
        payload = {
            'email': TEST_EMAIL,
            'password': 'testpassword',
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
        }
        user = get_user_model().objects.create_user(**payload)
        self.assertTrue(user.groups.filter(name=constants.Roles.READER).exists())

    def test_superuser_is_assigned__at_creation_to_admin_group_by_default(self):
        superuser = get_user_model().objects.create_superuser(email=TEST_EMAIL, password='testpassword')
        self.assertTrue(superuser.groups.filter(name=constants.Roles.ADMIN).exists())


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def test_create_valid_user_success(self):
        """Test create user with valid payload is successful"""
        payload = {
            'email': TEST_EMAIL,
            'password': 'testpassword',
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': TEST_EMAIL,
            'password': 'testpassword',
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
        }
        UserFactory(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': TEST_EMAIL, 'password': 'pw', 'first_name': TEST_FIRST_NAME, 'last_name': TEST_LAST_NAME}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        user_details = {
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'email': TEST_EMAIL,
            'password': 'test-user-pass123',
        }
        UserFactory(**user_details)

        payload = {'email': user_details['email'], 'password': user_details['password']}
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """Test that token is not create if invalid creds are given"""
        UserFactory(email=TEST_EMAIL, password='validpass')
        payload = {
            'email': TEST_EMAIL,
            'password': 'invalidpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
            'email': TEST_EMAIL,
            'password': 'testpassword',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test that email and password are required"""
        payload = {
            'email': TEST_EMAIL,
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self) -> None:
        self.user = UserFactory(
            email=TEST_EMAIL, password='testpass', first_name=TEST_FIRST_NAME, last_name=TEST_LAST_NAME
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {'first_name': self.user.first_name, 'last_name': self.user.last_name, 'email': self.user.email}
        )

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating profile for authenticated user"""
        payload = {'first_name': 'New first name', 'last_name': 'New last name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

import random
import time

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from user import constants
from user.factories import UserFactory

TEST_FIRST_NAME = 'Test first name'
TEST_LAST_NAME = 'Test last name'
TEST_EMAIL = 'test@test.com'
TEST_PASSWORD = 'test_pass123'


def pytest_collection_modifyitems(items):
    """Randomizes tests in order to prevent mutual dependencies."""

    # use current UNIX timestamp as seed
    seed = int(time.time())
    random.seed(seed)

    print(f"\npytest: randomizing tests order with seed = {seed}\n")  # noqa: T201

    random.shuffle(items)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    try:
        yield
    finally:
        cache.clear()


@pytest.fixture(autouse=True)
def fast_password_hashers(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def super_user():
    return UserFactory(is_superuser=True, role=constants.Roles.ADMIN)


@pytest.fixture
def admin_user():
    return UserFactory(role=constants.Roles.ADMIN)


@pytest.fixture
def librarian_user():
    return UserFactory(role=constants.Roles.LIBRARIAN)


@pytest.fixture
def reader_user():
    return UserFactory(role=constants.Roles.READER)


@pytest.fixture
def super_user_api_client(api_client, super_user):
    api_client.force_authenticate(user=super_user)
    return api_client


@pytest.fixture
def admin_user_api_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def librarian_user_api_client(api_client, librarian_user):
    api_client.force_authenticate(user=librarian_user)
    return api_client


@pytest.fixture
def reader_user_api_client(api_client, reader_user):
    api_client.force_authenticate(user=reader_user)
    return api_client


@pytest.fixture
def user_update_payload():
    return {
        'first_name': TEST_FIRST_NAME,
        'last_name': TEST_LAST_NAME,
        "password": TEST_PASSWORD,
    }

@pytest.fixture
def user_create_payload(user_update_payload):
    return {
        **user_update_payload,
        'email': TEST_EMAIL,
    }

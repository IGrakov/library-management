import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from user import constants
from user.factories import UserFactory

USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
USER_MANAGE_URL = reverse("user:manage")
USER_LIST_URL = reverse("user:list")

pytestmark = pytest.mark.django_db


def test_user_assigned_reader_group_by_default(user_create_payload):
    user = get_user_model().objects.create_user(**user_create_payload)

    assert user.groups.filter(name=constants.Roles.READER).exists()


def test_superuser_assigned_admin_group_by_default(user_create_payload):
    user_create_payload.pop("first_name")
    user_create_payload.pop("last_name")
    user = get_user_model().objects.create_superuser(**user_create_payload)

    assert user.groups.filter(name=constants.Roles.ADMIN).exists()


@pytest.mark.parametrize(
    ("url", "method", "payload"),
    (
        (USER_LIST_URL, "get", {}),
        (USER_CREATE_URL, "post", {"data": {}}),
        (USER_MANAGE_URL, "get", {}),
        (USER_MANAGE_URL, "put", {"data": {}}),
        (USER_MANAGE_URL, "patch", {"data": {}}),
        (f"{USER_MANAGE_URL}/1/", "get", {}),
        (f"{USER_MANAGE_URL}/1/", "put", {"data": {}}),
        (f"{USER_MANAGE_URL}/1/", "patch", {"data": {}}),
    ),
)
def test_user_endpoints_require_authentication(
    api_client,
    url,
    method,
    payload,
):
    response = getattr(api_client, method)(url, **payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_reader_user_not_allowed_to_list_users(auth_client, reader_user):
    response = auth_client(reader_user).get(USER_LIST_URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    ("user_fixture", "num_of_returned_records"),
    (
        ("super_user", 4),
        ("admin_user", 2),
        ("librarian_user", 1),
    ),
)
def test_admin_user_and_librarian_user_can_list_users_with_respective_role_ranks(
    user_fixture,
    request,
    auth_client,
    num_of_returned_records,
):
    user = request.getfixturevalue(user_fixture)

    UserFactory.create()
    UserFactory.create(role=constants.Roles.LIBRARIAN)
    UserFactory.create(role=constants.Roles.ADMIN)

    response = auth_client(user).get(USER_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == num_of_returned_records

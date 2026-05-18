from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from reader_card.factories import ReaderCardFactory
from reader_card.models import ReaderCard
from reference_values.factories import HallFactory
from reference_values.serializers import HallSerializer
from user import constants
from user.factories import UserFactory
from user.serializers import UserSerializer

CREATE_READER_CARD_URL = reverse("reader_card:create_reader_card")
LIST_READER_CARD_URL = reverse("reader_card:list_reader_card")

small_gif = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)


class PublicReaderCardApiTests(TestCase):
    """Test reader card API (public)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()

        self.photo = SimpleUploadedFile("reader_photo.jpg", small_gif, content_type="image/jpg")

    def test_create_reader_card_unauthenticated_fails(self):
        """Test creating a reader card by an unauthenticated user"""
        reader = UserFactory()
        hall = HallFactory()

        payload = {"reader": reader.id, "photo": self.photo, "hall_access": [hall.id]}

        res = self.client.post(CREATE_READER_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_reader_card_unauthenticated_fails(self):
        """Test retrieving a reader card by an unauthenticated user"""
        reader_card = ReaderCardFactory()

        res = self.client.get(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_reader_card_unauthenticated_fails(self):
        """Test deleting a reader card by an unauthenticated user"""
        reader_card = ReaderCardFactory()

        res = self.client.delete(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_reader_card_unauthenticated_fails(self):
        """Test updating a reader card by an unauthenticated user"""
        first_reader_card, second_reader_card = ReaderCardFactory.create_batch(2)

        hall_ids = [hall.id for hall in second_reader_card.hall_access.all()]

        payload = {"reader": first_reader_card.reader, "photo": second_reader_card.photo, "hall_access": hall_ids}

        res = self.client.put(reverse("reader_card:manage_reader_card", kwargs={"pk": first_reader_card.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reader_cards_unauthenticated_fails(self):
        """Test listing reader cards by an unauthenticated user"""
        ReaderCardFactory.create_batch(2)

        res = self.client.get(LIST_READER_CARD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReaderCardApiUserLibrarianTests(TestCase):
    """Test reader card API (private)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.LIBRARIAN)
        admin_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

        self.photo = SimpleUploadedFile("reader_photo.jpg", small_gif, content_type="image/jpg")

        self.maxDiff = None

    def test_create_reader_card_success(self):
        """Test creating a reader card by an authenticated user in librarian group"""

        reader = UserFactory()
        hall = HallFactory()

        payload = {"reader": reader.id, "photo": self.photo, "hall_access": [hall.id]}

        res = self.client.post(CREATE_READER_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        reader_cards = ReaderCard.objects.all()
        self.assertEqual(reader_cards.count(), 1)

    @override_settings(MEDIA_URL="")
    def test_retrieve_reader_card_success(self):
        """Test retrieving a reader card by an authenticated user in librarian group"""
        reader_card = ReaderCardFactory()

        res = self.client.get(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        expected_data = {
            "id": reader_card.id,
            "reader": UserSerializer(reader_card.reader).data,
            "photo": f"http://testserver/{reader_card.photo.name}",
            "is_suspended": reader_card.is_suspended,
            "hall_access": HallSerializer(reader_card.hall_access, many=True).data,
        }
        self.assertEqual(res.json(), expected_data)

    def test_delete_reader_card_success(self):
        """Test deleting a reader card by an authenticated user in librarian group"""
        reader_card = ReaderCardFactory()

        res = self.client.delete(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ReaderCard.objects.filter(id=reader_card.id).first(), None)

    def test_partial_update_reader_card_success(self):
        """Test partially updating a reader card by an authenticated user in librarian group"""
        first_reader_card, second_reader_card = ReaderCardFactory.create_batch(2)
        hall_ids = [hall.id for hall in second_reader_card.hall_access.all()]
        payload = {"hall_access": hall_ids}

        res = self.client.patch(reverse("reader_card:manage_reader_card", kwargs={"pk": first_reader_card.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_reader_card = ReaderCard.objects.filter(id=first_reader_card.id).first()

        updated_hall_ids = [hall.id for hall in updated_reader_card.hall_access.all()]
        self.assertEqual(updated_hall_ids, hall_ids)

    def test_full_update_reader_card_success(self):
        """Test updating a reader card by an authenticated user in librarian group"""
        first_reader_card, second_reader_card = ReaderCardFactory.create_batch(2)
        hall_ids = [hall.id for hall in second_reader_card.hall_access.all()]
        payload = {"photo": second_reader_card.photo, "is_suspended": True, "hall_access": hall_ids}

        res = self.client.put(reverse("reader_card:manage_reader_card", kwargs={"pk": first_reader_card.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_reader_card = ReaderCard.objects.filter(id=first_reader_card.id).first()

        updated_hall_ids = [hall.id for hall in updated_reader_card.hall_access.all()]
        self.assertEqual(updated_hall_ids, hall_ids)
        self.assertEqual(updated_reader_card.is_suspended, True)

    def test_list_reader_cards_success(self):
        """Test listing reader cards by an authenticated user in librarian group"""
        ReaderCardFactory.create_batch(2)

        res = self.client.get(LIST_READER_CARD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 2)


class PrivateReaderCardApiUserAdminOrReaderTests(TestCase):
    """Test reader card API (private)"""

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        admin_group, _ = Group.objects.get_or_create(name=constants.Roles.ADMIN)
        admin_group.user_set.add(self.user.id)
        reader_group, _ = Group.objects.get_or_create(name=constants.Roles.READER)
        reader_group.user_set.add(self.user.id)
        self.client.force_authenticate(user=self.user)

        self.photo = SimpleUploadedFile("reader_photo.jpg", small_gif, content_type="image/jpg")

        self.maxDiff = None

    def test_create_reader_card_fail(self):
        """Test creating a reader card by an authenticated user in admin or reader group"""

        reader = UserFactory()
        hall = HallFactory()

        payload = {"reader": reader.id, "photo": self.photo, "hall_access": [hall.id]}

        res = self.client.post(CREATE_READER_CARD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_reader_card_fail(self):
        """Test retrieving a reader card by an authenticated user in admin or reader group"""
        reader_card = ReaderCardFactory()

        res = self.client.get(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_reader_card_fail(self):
        """Test deleting a reader card by an authenticated user in admin or reader group"""
        reader_card = ReaderCardFactory()

        res = self.client.delete(reverse("reader_card:manage_reader_card", kwargs={"pk": reader_card.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reader_card_fail(self):
        """Test updating a reader card by an authenticated user in admin or reader group"""
        first_reader_card, second_reader_card = ReaderCardFactory.create_batch(2)
        hall_ids = [hall.id for hall in second_reader_card.hall_access.all()]
        payload = {"photo": second_reader_card.photo, "is_suspended": True, "hall_access": hall_ids}

        res = self.client.put(reverse("reader_card:manage_reader_card", kwargs={"pk": first_reader_card.id}), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_reader_cards_fail(self):
        """Test listing reader cards by an authenticated user in admin or reader group"""
        ReaderCardFactory.create_batch(2)

        res = self.client.get(LIST_READER_CARD_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

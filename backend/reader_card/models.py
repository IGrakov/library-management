from django.db import models
from django.db.models import QuerySet

from book.models import BookLoan
from core.models import TimeStampMixin
from reference_values.models import Hall
from user.models import User


class ReaderCard(TimeStampMixin):
    """Model for card of a library reader"""

    reader = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader_card")
    is_suspended = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="reader_card_photos/", blank=True)
    hall_access = models.ManyToManyField(Hall, related_name="reader_cards", blank=True)

    @property
    def active_loans(self) -> QuerySet[BookLoan]:
        return self.book_loans.filter(returned_at__isnull=True)

    def __str__(self) -> str:
        return f"{self.reader.last_name} {self.reader.first_name}"

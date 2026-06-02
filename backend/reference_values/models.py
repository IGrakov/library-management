from django.db import models

from core.models import TimeStampMixin


class Language(TimeStampMixin):
    """Model for reference value of language consisting of ISO639
    language name and two- and three-letter code"""

    name = models.CharField(max_length=255, unique=True)
    two_letter_code = models.CharField(max_length=2, unique=True)
    three_letter_code = models.CharField(max_length=3, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Language"


class Genre(TimeStampMixin):
    """Model for reference value of book genre"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Genre"


class Hall(TimeStampMixin):
    """Model for a library hall"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Hall"


class Author(TimeStampMixin):
    """Model for an author"""

    last_name = models.CharField(max_length=100, db_index=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)  # noqa: DJ001
    middle_name = models.CharField(max_length=100, null=True, blank=True)  # noqa: DJ001

    def __str__(self) -> str:
        return ", ".join(filter(None, [self.last_name, " ".join(filter(None, [self.first_name, self.middle_name]))]))

    class Meta:
        verbose_name = "Author"

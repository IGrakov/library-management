from django.db import models

from core.models import TimeStampMixin


class Language(TimeStampMixin):
    """Model for reference value of language consisting of ISO639
    language name and two- and three-letter code"""

    name = models.CharField(max_length=255)
    two_letter_code = models.CharField(max_length=2)
    three_letter_code = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Language"


class Genre(TimeStampMixin):
    """Model for reference value of book genre"""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Genre"


class Hall(TimeStampMixin):
    """Model for a library hall"""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Hall"

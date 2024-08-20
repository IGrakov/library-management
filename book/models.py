from django.db import models

from core.models import TimeStampMixin


class Book(TimeStampMixin):
    """Model for a book"""

    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    published_date = models.DateField(null=True)
    isbn = models.CharField(max_length=255, null=False, blank=False, unique=True)
    pages = models.IntegerField(null=True)
    cover = models.URLField(null=True)
    language = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return (
            f"{self.title} - by {self.author} - ISBN: {self.isbn} - in {self.language}"
        )

    class Meta:
        verbose_name = 'Book'

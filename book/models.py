from django.db import models

from core.models import TimeStampMixin
from reference_values.models import Language


class Author(TimeStampMixin):
    """Model for an author"""
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ", ".join(filter(None, [self.last_name, " ".join(filter(None, [self.first_name, self.middle_name]))]))

    class Meta:
        verbose_name = 'Author'


class Book(TimeStampMixin):
    """Model for a book"""
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.ManyToManyField(Author)
    published_date = models.DateField(null=True)
    isbn = models.CharField(max_length=17, null=False, blank=False, unique=True)
    pages = models.IntegerField(null=True)
    cover = models.URLField(null=True)
    language = models.ManyToManyField(Language)

    def __str__(self):
        return (
            f"{self.title} - by {self.author} - ISBN: {self.isbn} - in {self.language}"
        )

    class Meta:
        verbose_name = 'Book'

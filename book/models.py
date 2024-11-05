from django.db import models

from core.models import TimeStampMixin
from reference_values.models import Genre, Language


class Author(TimeStampMixin):
    """Model for an author"""

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return ', '.join(filter(None, [self.last_name, ' '.join(filter(None, [self.first_name, self.middle_name]))]))

    class Meta:
        verbose_name = 'Author'


class Book(TimeStampMixin):
    """Model for a book"""

    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.ManyToManyField(Author, blank=True, related_name='books')
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=17, null=False, blank=False, unique=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    language = models.ManyToManyField(Language, blank=True, related_name='books')
    genre = models.ManyToManyField(Genre, blank=True, related_name='books')

    def __str__(self):
        author_lst = []
        for author in self.author.all():
            # join first_name and middle_name only if they are not none
            author_lst.append(' '.join(filter(None, [author.last_name, author.first_name, author.middle_name])))
        authors = ', '.join(author_lst)

        language_lst = []
        for language in self.language.all():
            language_lst.append(f'{language.two_letter_code}')
        languages = ', '.join(language_lst)

        genre_lst = []
        for genre in self.genre.all():
            genre_lst.append(f'{genre.name}')
        genres = ', '.join(genre_lst)

        return f'{self.title} - by {authors} - ISBN: {self.isbn} - in {languages} - in {genres}'

    class Meta:
        verbose_name = 'Book'

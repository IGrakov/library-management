import uuid

from django.db import models
from django.db.models import Q, UniqueConstraint

from core.models import TimeStampMixin
from reader_card.models import ReaderCard
from reference_values.models import Author, Genre, Hall, Language


class Book(TimeStampMixin):
    """Model for a book"""

    title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    author = models.ManyToManyField(Author, blank=True, related_name="books")
    published_date = models.DateField(null=True, blank=True, db_index=True)
    isbn = models.CharField(max_length=17, null=False, blank=False, unique=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)  # noqa: DJ001
    language = models.ManyToManyField(Language, blank=True, related_name="books")
    genre = models.ManyToManyField(Genre, blank=True, related_name="books")

    def __str__(self) -> str:
        author_lst = []
        for author in self.author.all():
            # join first_name and middle_name only if they are not none
            author_lst.append(" ".join(filter(None, [author.last_name, author.first_name, author.middle_name])))
        authors = ", ".join(author_lst)

        language_lst = [f"{language.two_letter_code}" for language in self.language.all()]
        languages = ", ".join(language_lst)

        genre_lst = [f"{genre.name}" for genre in self.genre.all()]
        genres = ", ".join(genre_lst)

        return f"{self.title} - by {authors} - ISBN: {self.isbn} - in {languages} - in {genres}"

    class Meta:
        verbose_name = "Book"


class BookCopy(TimeStampMixin):
    """Model for a book copy (with the same ISBN)"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_available(self) -> bool:
        return not self.book_loans.filter(returned_at__isnull=True).exists()

    def __str__(self) -> str:
        return f"Copy of book with ISBN {self.book.isbn} with uid {self.uid}"

    class Meta:
        verbose_name = "Book copy"
        verbose_name_plural = "Book copies"


class BookLoan(TimeStampMixin):
    """Model for a book loan"""

    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name="book_loans")
    reader_card = models.ForeignKey(ReaderCard, on_delete=models.CASCADE, related_name="book_loans")

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(db_index=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Book loan"

        constraints = (
            UniqueConstraint(
                fields=["book_copy"],
                condition=Q(returned_at__isnull=True),
                name="unique_active_loan_per_copy",
            ),
        )

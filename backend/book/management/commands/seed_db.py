import factory
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from book.models import Author, Book, BookCopy
from reference_values.constants import HallTypes, GenreTypes
from reference_values.models import Genre, Language, Hall

from book.factories import (
    AuthorFactory,
    BookFactory,
    BookCopyFactory,
)
from reference_values.factories import (
    LanguageFactory,
)

AUTHOR_COUNT_DIST = [
    (1, 0.75),
    (2, 0.2),
    (3, 0.05),
]

LANGUAGE_COUNT_DIST = [
    (1, 0.9),
    (2, 0.1),
]

GENRE_COUNT_DIST = [
    (1, 0.6),
    (2, 0.3),
    (3, 0.1),
]


class Command(BaseCommand):
    help = "Seed database with test data"

    def weighted_choice(self, choices_with_weights):
        choices, weights = zip(*choices_with_weights)
        return random.choices(choices, weights=weights, k=1)[0]

    def pick_count(self, distribution):
        """
        distribution = [(value, weight), ...]
        """
        return self.weighted_choice(distribution)

    def pick_weighted_subset(self, items, count, weights=None):
        """
        Pick count` items with bias (no duplicates)
        """
        if not items:
            return []

        if weights is None:
            weights = [1] * len(items)

        selected = set()
        while len(selected) < min(count, len(items)):
            selected.add(random.choices(items, weights=weights, k=1)[0])

        return list(selected)

    def generate_weights(self, items, skew_strength=2.0):
        """
        Higher skew_strength → more inequality
        """
        return [random.random() ** skew_strength for _ in items]

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=int, default=10)
        parser.add_argument("--books", type=int, default=20)
        parser.add_argument("--languages", type=int, default=5)
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing database...")
            BookCopy.objects.all().delete()
            Book.objects.all().delete()
            Author.objects.all().delete()
            Genre.objects.all().delete()
            Language.objects.all().delete()
            Hall.objects.all().delete()

        self.stdout.write("Creating reference data...")

        self.stdout.write("Creating halls...")
        halls = []
        for hall_type in HallTypes:
            hall, _ = Hall.objects.get_or_create(name=hall_type.value)
            halls.append(hall)

        self.stdout.write("Creating genres...")
        genres = []
        for genre_type in GenreTypes:
            genre, _ = Genre.objects.get_or_create(name=genre_type.value)
            genres.append(genre)

        self.stdout.write("Creating languages...")
        languages = LanguageFactory.create_batch(options["languages"])

        self.stdout.write("Creating authors...")
        authors = AuthorFactory.create_batch(options["authors"])

        self.stdout.write("Creating books and copies...")
        books = []

        author_weights = self.generate_weights(authors)
        language_weights = self.generate_weights(languages)
        genre_weights = self.generate_weights(genres)

        for _ in range(options["books"]):
            author_count = self.pick_count(AUTHOR_COUNT_DIST)
            language_count = self.pick_count(LANGUAGE_COUNT_DIST)
            genre_count = self.pick_count(GENRE_COUNT_DIST)

            book = BookFactory(
                author=self.pick_weighted_subset(authors, author_count, author_weights),
                language=self.pick_weighted_subset(languages, language_count, language_weights),
                genre=self.pick_weighted_subset(genres, genre_count, genre_weights),
            )
            books.append(book)

            num_copies = random.choices(
                [1, 2, 3, 5, 10],
                weights=[50, 25, 15, 7, 3],  # bias toward small numbers
                k=1
            )[0]

            BookCopyFactory.create_batch(
                num_copies,
                book=book,
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

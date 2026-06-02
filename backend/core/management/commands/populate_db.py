import random
from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from book.models import Book, BookCopy
from reader_card.models import ReaderCard
from reference_values.constants import HallTypes
from reference_values.models import Author, Genre, Hall, Language
from user.constants import Roles
from user.factories import UserFactory
from user.models import User

NUM_OF_ADMINS = 10
NUM_OF_LIBRARIANS = 10
NUM_OF_READERS = 2_000
NUM_OF_AUTHORS = 5_000
NUM_OF_BOOKS = 100_000
MIDDLE_NAME_PROBABILITY = 0.2

fake = Faker()


class Command(BaseCommand):
    help = "Populates database with random generated data"

    def add_arguments(self, parser) -> None:  # noqa: ANN001
        parser.add_argument("--readers", type=int, default=NUM_OF_READERS)
        parser.add_argument("--authors", type=int, default=NUM_OF_AUTHORS)
        parser.add_argument("--books", type=int, default=NUM_OF_BOOKS)

        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before seeding",
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ARG002, ANN401
        if options["flush"]:
            self.stdout.write("Flushing database...")
            User.objects.filter(is_superuser=False).delete()
            BookCopy.objects.all().delete()
            Book.objects.all().delete()
            Author.objects.all().delete()

        # # populate database with user groups
        Group.objects.get_or_create(name=Roles.READER)
        Group.objects.get_or_create(name=Roles.LIBRARIAN)

        # # populate database with users
        def create_users(count: int, role: str = Roles.READER) -> None:
            start_id = User.objects.last().id + 1 if User.objects.exists() else 0
            for i in range(count):
                first_name = fake.first_name()
                last_name = fake.last_name()

                UserFactory(
                    first_name=first_name,
                    last_name=last_name,
                    email=f"{first_name}.{last_name}{start_id + i}@google.com",
                    role=role,
                )

        create_users(NUM_OF_ADMINS, Roles.ADMIN)
        create_users(NUM_OF_LIBRARIANS, Roles.LIBRARIAN)
        create_users(NUM_OF_READERS)

        self.stdout.write(self.style.SUCCESS("Successfully created users"))

        # populate database with languages
        languages = [
            {"name": "Czech", "two_letter_code": "cs", "three_letter_code": "cze"},
            {"name": "Danish", "two_letter_code": "da", "three_letter_code": "dan"},
            {"name": "Dutch", "two_letter_code": "nl", "three_letter_code": "dut"},
            {"name": "English", "two_letter_code": "en", "three_letter_code": "eng"},
            {"name": "Finnish", "two_letter_code": "fi", "three_letter_code": "fin"},
            {"name": "French", "two_letter_code": "fr", "three_letter_code": "fra"},
            {"name": "German", "two_letter_code": "de", "three_letter_code": "deu"},
            {"name": "Greek", "two_letter_code": "el", "three_letter_code": "gre"},
            {"name": "Hindi", "two_letter_code": "hi", "three_letter_code": "hin"},
            {"name": "Italian", "two_letter_code": "it", "three_letter_code": "ita"},
            {"name": "Japanese", "two_letter_code": "ja", "three_letter_code": "jpn"},
            {"name": "Korean", "two_letter_code": "ko", "three_letter_code": "kor"},
            {"name": "Latin", "two_letter_code": "la", "three_letter_code": "lat"},
            {"name": "Polish", "two_letter_code": "pl", "three_letter_code": "pol"},
            {"name": "Portuguese", "two_letter_code": "pt", "three_letter_code": "por"},
            {"name": "Romanian", "two_letter_code": "ro", "three_letter_code": "rum"},
            {"name": "Spanish", "two_letter_code": "es", "three_letter_code": "spa"},
            {"name": "Swedish", "two_letter_code": "sv", "three_letter_code": "swe"},
        ]

        for language in languages:
            Language.objects.get_or_create(
                name=language["name"],
                two_letter_code=language["two_letter_code"],
                three_letter_code=language["three_letter_code"],
            )

        self.stdout.write(self.style.SUCCESS("Successfully created languages"))

        # populate database with genres
        genres = [
            "Fantasy",
            "Science Fiction",
            "Mystery",
            "Horror",
            "Romance",
            "Children's",
            "Science & Technology",
            "Humanities & Social Sciences",
            "Travel",
            "History",
            "Biography",
            "Memoir & Autobiography",
            "Thriller & Suspense",
            "Action & Adventure",
            "Detective",
            "Historical Fiction",
        ]

        for genre in genres:
            Genre.objects.get_or_create(name=genre)

        self.stdout.write(self.style.SUCCESS("Successfully created genres"))

        # populate database with halls
        for hall in HallTypes:
            Hall.objects.get_or_create(name=hall)

        self.stdout.write(self.style.SUCCESS("Successfully created halls"))

        # populate database with reader cards
        hall_choices = [1, 1, 2, 2, 2, 3, 4, 5]
        for reader in User.objects.all():
            if reader.groups.filter(name=Roles.READER).exists() and not ReaderCard.objects.filter(reader=reader):
                reader_card, created = ReaderCard.objects.get_or_create(reader=reader, photo=fake.file_path())

                if created:
                    num_of_halls = random.choice(hall_choices)  # noqa: S311
                    for _ in range(num_of_halls):
                        hall = Hall.objects.order_by("?").first()
                        reader_card.hall_access.add(hall)

        self.stdout.write(self.style.SUCCESS("Successfully created reader cards"))

        # populate database with authors
        for _ in range(NUM_OF_AUTHORS):
            last_name = fake.last_name()
            first_name = fake.first_name()
            middle_name = None
            rand_num = random.random()  # noqa: S311
            if rand_num < MIDDLE_NAME_PROBABILITY:
                middle_name = fake.first_name()

            Author.objects.get_or_create(last_name=last_name, first_name=first_name, middle_name=middle_name)

        self.stdout.write(self.style.SUCCESS("Successfully created authors"))

        # populate database with books
        existing_isbns = set(Book.objects.all().values_list("isbn", flat=True))
        new_isbns = set()
        for _ in range(NUM_OF_BOOKS):
            isbn = fake.isbn13()
            if isbn not in existing_isbns:
                new_isbns.add(isbn)

        self.stdout.write(self.style.SUCCESS("Successfully created unique ISBNs"))

        author_choices = [1, 1, 1, 1, 2, 2, 3]  # to ensure unequal distribution of choices
        language_choices = [1, 1, 1, 1, 1, 2, 3]
        genre_choices = [1, 1, 1, 1, 1, 1, 2]
        for isbn in new_isbns:
            title_length = random.randint(1, 5)  # noqa: S311
            title = fake.sentence(nb_words=title_length)[:-1]
            published_date = fake.date()
            pages = random.randint(10, 1_000)  # noqa: S311
            cover = fake.image_url()
            book, created = Book.objects.get_or_create(
                title=title,
                published_date=published_date,
                isbn=isbn,
                pages=pages,
                cover=cover,
            )

            if created:
                num_of_authors = random.choice(author_choices)  # noqa: S311
                num_of_languages = random.choice(language_choices)  # noqa: S311
                num_of_genres = random.choice(genre_choices)  # noqa: S311

                for _ in range(num_of_authors):
                    author = Author.objects.order_by("?").first()
                    book.author.add(author)

                for _ in range(num_of_languages):
                    language = Language.objects.order_by("?").first()
                    book.language.add(language)

                for _ in range(num_of_genres):
                    genre = Genre.objects.order_by("?").first()
                    book.genre.add(genre)

                book.save()

        self.stdout.write(self.style.SUCCESS("Successfully created books"))

        # populate database with book copies
        books = Book.objects.all()

        book_copy_choices = [1, 1, 1, 1, 2, 2, 2, 3, 4]

        for book in books:
            num_of_copies = random.choice(book_copy_choices)  # noqa: S311
            book_copies = []
            for _ in range(num_of_copies):
                book_copies.append(BookCopy(book=book, uid=fake.uuid4()))
            BookCopy.objects.bulk_create(book_copies)

        self.stdout.write(self.style.SUCCESS("Successfully created book copies"))

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))

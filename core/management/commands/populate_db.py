import random
from faker import Faker

from django.core.management.base import BaseCommand

from book.models import Author, Book, BookCopy
from reference_values.models import Genre, Language

NUM_OF_AUTHORS = 20
NUM_OF_BOOKS = 100
MIDDLE_NAME_PROBABILITY = 0.2

fake = Faker()


class Command(BaseCommand):
    help = "Populates database with random generated data"

    def handle(self, *args, **options):

        # populate database with languages
        languages = [
            {'name': 'Czech', 'two_letter_code': 'cs', 'three_letter_code': 'cze'},
            {'name': 'Danish', 'two_letter_code': 'da', 'three_letter_code': 'dan'},
            {'name': 'Dutch', 'two_letter_code': 'nl', 'three_letter_code': 'dut'},
            {'name': 'English', 'two_letter_code': 'en', 'three_letter_code': 'eng'},
            {'name': 'Finnish', 'two_letter_code': 'fi', 'three_letter_code': 'fin'},
            {'name': 'French', 'two_letter_code': 'fr', 'three_letter_code': 'fra'},
            {'name': 'German', 'two_letter_code': 'de', 'three_letter_code': 'deu'},
            {'name': 'Greek', 'two_letter_code': 'el', 'three_letter_code': 'gre'},
            {'name': 'Hindi', 'two_letter_code': 'hi', 'three_letter_code': 'hin'},
            {'name': 'Italian', 'two_letter_code': 'it', 'three_letter_code': 'ita'},
            {'name': 'Japanese', 'two_letter_code': 'ja', 'three_letter_code': 'jpn'},
            {'name': 'Korean', 'two_letter_code': 'ko', 'three_letter_code': 'kor'},
            {'name': 'Latin', 'two_letter_code': 'la', 'three_letter_code': 'lat'},
            {'name': 'Polish', 'two_letter_code': 'pl', 'three_letter_code': 'pol'},
            {'name': 'Portuguese', 'two_letter_code': 'pt', 'three_letter_code': 'por'},
            {'name': 'Romanian', 'two_letter_code': 'ro', 'three_letter_code': 'rum'},
            {'name': 'Spanish', 'two_letter_code': 'es', 'three_letter_code': 'spa'},
            {'name': 'Swedish', 'two_letter_code': 'sv', 'three_letter_code': 'swe'},
        ]

        for language in languages:
            Language.objects.get_or_create(
                name=language['name'],
                two_letter_code=language['two_letter_code'],
                three_letter_code=language['three_letter_code'],
            )


        # populate database with genres
        genres = [
            'Fantasy', 'Science Fiction', 'Mystery', 'Horror', 'Romance', 'Children\'s', 'Science & Technology',
            'Humanities & Social Sciences', 'Travel', 'History', 'Biography', 'Memoir & Autobiography',
            'Thriller & Suspense', 'Action & Adventure', 'Detective', 'Historical Fiction',
        ]

        for genre in genres:
            Genre.objects.get_or_create(name=genre)


        # populate database with authors
        for _ in range(NUM_OF_AUTHORS):
            last_name = fake.last_name()
            first_name = fake.first_name()
            middle_name = None
            rand_num = random.random()
            if rand_num < MIDDLE_NAME_PROBABILITY:
                middle_name = fake.first_name()

            Author.objects.get_or_create(last_name=last_name, first_name=first_name, middle_name=middle_name)


        # populate database with books
        author_choices = [1, 1, 1, 1, 2, 2, 3]  # to ensure unequal distribution of choices
        language_choices = [1, 1, 1, 1, 1, 2, 3]
        genre_choices = [1, 1, 1, 1, 1, 1, 2]
        for _ in range(NUM_OF_BOOKS):
            title_length = random.randint(1, 5)
            title = fake.sentence(nb_words=title_length)[:-1]
            published_date = fake.date()
            isbn = fake.isbn13()
            pages = random.randint(10, 1_000)
            cover = fake.image_url()
            book, created = Book.objects.get_or_create(title=title, published_date=published_date, isbn=isbn, pages=pages, cover=cover)

            if created:
                num_of_authors = random.choice(author_choices)
                num_of_languages = random.choice(language_choices)
                num_of_genres = random.choice(genre_choices)

                for _ in range(num_of_authors):
                    author = Author.objects.order_by('?').first()
                    book.author.add(author)

                for _ in range(num_of_languages):
                    language = Language.objects.order_by('?').first()
                    book.language.add(language)

                for _ in range(num_of_genres):
                    genre = Genre.objects.order_by('?').first()
                    book.genre.add(genre)

                book.save()


        # populate database with book copies

        books = Book.objects.all()

        book_copy_choices = [1, 1, 1, 1, 2, 2, 2, 3, 4]

        for book in books:
            num_of_copies = random.choice(book_copy_choices)
            book_copies = []
            for _ in range(num_of_copies):
                book_copies.append(BookCopy(
                    book=book,
                    uid = fake.uuid4()
                ))
            BookCopy.objects.bulk_create(book_copies)


        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))

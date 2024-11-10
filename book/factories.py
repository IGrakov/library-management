import random

import factory

from book.models import Author, Book, BookCopy
from reference_values.factories import GenreFactory, LanguageFactory


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    last_name = factory.Faker('last_name')
    first_name = factory.Faker('first_name')
    middle_name = factory.Faker('first_name')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=5, variable_nb_words=True)
    published_date = factory.Faker('date')
    isbn = factory.Faker('isbn13')
    pages = factory.Faker('pyint', min_value=10, max_value=1_000)
    cover = factory.Faker('image_url')

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.author.add(*extracted)
        else:
            num_of_authors = random.randint(1, 3)
            self.author.add(*AuthorFactory.create_batch(num_of_authors))

    @factory.post_generation
    def language(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.language.add(*extracted)
        else:
            num_of_languages = random.randint(1, 3)
            self.language.add(*LanguageFactory.create_batch(num_of_languages))

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.genre.add(*extracted)
        else:
            num_of_genres = random.randint(1, 3)
            self.genre.add(*GenreFactory.create_batch(num_of_genres))


class BookCopyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookCopy

    book = factory.SubFactory(BookFactory)
    uid = factory.Faker('uuid4')

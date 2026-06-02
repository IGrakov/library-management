from random import randint
from typing import Any, Iterable

import factory

from book.models import Book, BookCopy
from reference_values.factories import AuthorFactory, GenreFactory, LanguageFactory
from reference_values.models import Author, Genre, Language


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    published_date = factory.Faker("date")
    isbn = factory.Faker("isbn13")
    pages = factory.Faker("pyint", min_value=10, max_value=1_000)
    cover = factory.Faker("image_url")

    @factory.post_generation
    def author(self, create: bool, extracted: Iterable[Author], **kwargs: Any) -> None:  # noqa: ARG002, ANN401
        if not create:
            return

        if extracted:
            self.author.add(*extracted)
        else:
            num_of_authors = randint(1, 3)  # noqa: S311
            self.author.add(*AuthorFactory.create_batch(num_of_authors))

    @factory.post_generation
    def language(self, create: bool, extracted: Iterable[Language], **kwargs: Any) -> None:  # noqa: ARG002, ANN401
        if not create:
            return

        if extracted:
            self.language.add(*extracted)
        else:
            num_of_languages = randint(1, 3)  # noqa: S311
            self.language.add(*LanguageFactory.create_batch(num_of_languages))

    @factory.post_generation
    def genre(self, create: bool, extracted: Iterable[Genre], **kwargs: Any) -> None:  # noqa: ARG002, ANN401
        if not create:
            return

        if extracted:
            self.genre.add(*extracted)
        else:
            num_of_genres = randint(1, 3)  # noqa: S311
            self.genre.add(*GenreFactory.create_batch(num_of_genres))


class BookCopyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookCopy

    book = factory.SubFactory(BookFactory)

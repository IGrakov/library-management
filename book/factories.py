import random

import factory

from book.models import Author, Book
from reference_values.factories import LanguageFactory


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
    isbn = factory.Sequence(lambda n: f'{n}-{n}-{n}-{n}-{n}'[:17])
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

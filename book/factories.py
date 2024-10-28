import factory

from book.models import Author, Book
from reference_values.factories import LanguageFactory


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    last_name = factory.Faker('last_name')
    first_name = factory.Faker('first_name')
    middle_name = factory.Faker('middle_name')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.SubFactory(AuthorFactory)
    author = factory.Faker('name')
    published_date = factory.Faker('date')
    isbn = factory.Sequence(lambda n: f'{n}-{n}-{n}-{n}-{n}')
    pages = factory.Faker('pyint', min_value=10, max_value=1_000)
    cover = factory.Faker('image_url')
    language = factory.SubFactory(LanguageFactory)

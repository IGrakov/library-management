import factory

from book.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence')
    author = factory.Faker('name')
    published_date = factory.Faker('date')
    isbn = factory.Sequence(lambda n: f'{n}-{n}-{n}-{n}-{n}')
    pages = factory.Faker('pyint', min_value=10, max_value=1_000)
    cover = factory.Faker('image_url')
    language = factory.Faker('language_name')

import random

import factory

from reference_values.constants import HallTypes
from reference_values.models import Genre, Hall, Language


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    name = factory.Faker('language_name')
    two_letter_code = factory.LazyAttribute(lambda a: a.name[:2].lower())
    three_letter_code = factory.LazyAttribute(lambda a: a.name[:3].lower())


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker('word')


class HallFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hall

    name = factory.LazyFunction(lambda: random.choice([el for el in HallTypes]))  # noqa C416

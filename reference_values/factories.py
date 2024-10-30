import factory

from reference_values.models import Language


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    name = factory.Faker('language_name')
    two_letter_code = factory.LazyAttribute(lambda a: a.name[:2].lower())
    three_letter_code = factory.LazyAttribute(lambda a: a.name[:3].lower())

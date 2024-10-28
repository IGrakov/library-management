import factory

from reference_values.models import Language


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    name = factory.Faker('language_name')
    two_letter_code = name[:2].upper()
    three_letter_code = name[:3].upper()

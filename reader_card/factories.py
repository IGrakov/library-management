from random import randint

import factory

from reader_card.models import ReaderCard
from reference_values.factories import HallFactory
from user.factories import UserFactory


class ReaderCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReaderCard

    reader = factory.SubFactory(UserFactory)
    photo = factory.django.ImageField()

    @factory.post_generation
    def hall_access(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.hall_access.add(*extracted)
        else:
            num_of_halls = randint(1, 3)
            self.hall_access.add(*HallFactory.create_batch(num_of_halls))

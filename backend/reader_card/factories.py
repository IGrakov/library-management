from random import randint
from typing import Any, Iterable

import factory

from reader_card.models import ReaderCard
from reference_values.factories import HallFactory
from reference_values.models import Hall
from user.factories import UserFactory


class ReaderCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReaderCard

    reader = factory.SubFactory(UserFactory)
    photo = factory.django.ImageField()

    @factory.post_generation
    def hall_access(self, create: bool, extracted: Iterable[Hall], **kwargs: Any):  # noqa: ARG002, ANN401
        if not create:
            return

        if extracted:
            self.hall_access.add(*extracted)
        else:
            num_of_halls = randint(1, 3)  # noqa: S311
            self.hall_access.add(*HallFactory.create_batch(num_of_halls))

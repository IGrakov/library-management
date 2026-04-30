import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from user import constants

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.LazyAttribute(lambda o: '%s@test.com' % f'{o.first_name}.{o.last_name}')
    first_name = factory.Sequence(lambda n: 'first_name%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name%s' % n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        role = kwargs.pop("role", constants.Roles.READER)
        user = model_class(*args, **kwargs)
        user.set_password(kwargs.get("password", "password123"))

        user.is_staff = role in {constants.Roles.ADMIN, constants.Roles.LIBRARIAN}
        user.save()

        user.groups.clear()

        if not user.is_superuser:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        return user

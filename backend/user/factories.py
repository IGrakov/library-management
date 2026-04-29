import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from user import constants

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.LazyAttribute(lambda o: '%s@test.com' % f'{o.first_name}.{o.last_name}')
    first_name = factory.Sequence(lambda n: 'first_name%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name%s' % n)
    password = factory.django.Password('password123')

    role = constants.Roles.READER

    @factory.post_generation
    def assign_role(self, create, extracted, **kwargs):
        if not create:
            return

        role = extracted or self.role

        group = Group.objects.get(name=role)
        self.groups.add(group)

        if role in {constants.Roles.ADMIN, constants.Roles.LIBRARIAN}:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False

        self.save()

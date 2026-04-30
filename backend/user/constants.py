from django.db import models


class Roles(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    READER = 'Reader', 'Reader'
    LIBRARIAN = 'Librarian', 'Librarian'

INACTIVE_USER_RANK = -1
SUPER_USER_RANK = 100
ADMIN_USER_RANK = 20
LIBRARIAN_USER_RANK = 10
READER_USER_RANK = 0

from django.db import models


class Roles(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    READER = 'Reader', 'Reader'
    LIBRARIAN = 'Librarian', 'Librarian'

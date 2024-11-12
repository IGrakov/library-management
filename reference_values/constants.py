from django.db import models


class HallTypes(models.TextChoices):
    LOANS = 'Loans', 'Loans'
    PERIODICALS = 'Periodicals', 'Periodicals'
    READING_HALL = 'Reading Hall', 'Reading Hall'
    RARITIES = 'Rarities', 'Rarities'
    WAREHOUSE = 'Warehouse', 'Warehouse'

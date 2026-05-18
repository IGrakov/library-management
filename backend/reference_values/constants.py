from django.db import models


class HallTypes(models.TextChoices):
    LOANS = "Loans", "Loans"
    PERIODICALS = "Periodicals", "Periodicals"
    READING_HALL = "Reading Hall", "Reading Hall"
    RARITIES = "Rarities", "Rarities"
    WAREHOUSE = "Warehouse", "Warehouse"


class GenreTypes(models.TextChoices):
    FICTION = "Fiction", "Fiction"
    NON_FICTION = "Non-Fiction", "Non-Fiction"
    FANTASY = "Fantasy", "Fantasy"
    TRAVEL = (
        "Travel",
        "Travel",
    )
    HISTORY = (
        "History",
        "History",
    )
    BIOGRAPHY = (
        "Biography",
        "Biography",
    )
    ROMANCE = (
        "Romance",
        "Romance",
    )
    MUSIC = (
        "Music",
        "Music",
    )
    SCIENCE_FICTION = (
        "Science Fiction",
        "Science Fiction",
    )
    POETRY = (
        "Poetry",
        "Poetry",
    )
    CHILDREN = (
        "Children",
        "Children",
    )
    RELIGION = (
        "Religion",
        "Religion",
    )
    SCIENCE_TECHNOLOGY = (
        "Science & Technology",
        "Science & Technology",
    )
    SOCIAL_SCIENCE = (
        "Social Science",
        "Social Science",
    )
    HOW_TO = (
        "How-To",
        "How-To",
    )
    HUMOR = (
        "Humor",
        "Humor",
    )
    CRIME = (
        "Crime",
        "Crime",
    )
    ART = (
        "Art",
        "Art",
    )
    FOOD_DRINK = (
        "Food & Drink",
        "Food & Drink",
    )
    ACTION_ADVENTURE = (
        "Action & Adventure",
        "Action & Adventure",
    )
    MISTERY = (
        "Mystery",
        "Mystery",
    )
    THRILLER_SUSPENSE = (
        "Thriller & Suspense",
        "Thriller & Suspense",
    )
    HORROR = "Horror", "Horror"

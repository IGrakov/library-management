from rest_framework import serializers

from book.models import Author, Book
from reference_values.serializers import LanguageSerializer


class AuthorSerializer(serializers.ModelSerializer):
    model = Author
    fields = [
        'id',
        'last_name',
        'first_name',
        'middle_name',
    ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    language = LanguageSerializer()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'published_date',
            'isbn',
            'pages',
            'cover',
            'language',
        ]

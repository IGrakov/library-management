from django.db.transaction import atomic
from rest_framework import serializers

from book.models import Author, Book
from reference_values.models import Language
from reference_values.serializers import LanguageSerializer


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author

        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
        ]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)

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


class BookWriteSerializer(serializers.ModelSerializer):
    author = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    language = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    def validate(self, attrs):
        book_attrs = {**attrs}
        book_attrs.pop('author', [])
        book_attrs.pop('language', [])

        return attrs

    @staticmethod
    def add_authors_and_languages(instance, author_ids, language_ids):
        for author_id in author_ids:
            author = Author.objects.filter(id=author_id).first()
            # Ignore if author id in payload is invalid
            if author:
                instance.author.add(author)
        for language_id in language_ids:
            language = Language.objects.filter(id=language_id).first()
            # Ignore if language id in payload is invalid
            if language:
                instance.language.add(language)

    @atomic
    def create(self, validated_data):
        author_ids = validated_data.pop('author', [])
        language_ids = validated_data.pop('language', [])

        book = Book.objects.create(**validated_data)

        self.add_authors_and_languages(book, author_ids, language_ids)

        return book

    @atomic
    def update(self, instance, validated_data):
        author_ids = validated_data.pop('author', [])
        language_ids = validated_data.pop('language', [])

        instance = super().update(instance, validated_data)

        # Do not remove author references in case that payload for partial update does not contain any authors
        if author_ids:
            instance.author.remove(*instance.author.all())
        # Do not remove language references in case that payload for partial update does not contain any languages
        if language_ids:
            instance.language.remove(*instance.language.all())

        self.add_authors_and_languages(instance, author_ids, language_ids)

        return instance

    def to_representation(self, data):
        return BookSerializer(context=self.context).to_representation(data)

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

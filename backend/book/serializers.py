from django.db.transaction import atomic
from rest_framework import serializers

from book.models import Author, Book, BookCopy
from reference_values.models import Genre, Language
from reference_values.serializers import GenreSerializer, LanguageSerializer


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
    genre = GenreSerializer(many=True, read_only=True)

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
            'genre',
        ]


class BookWriteSerializer(serializers.ModelSerializer):
    author = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    language = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    genre = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    def validate(self, attrs):
        book_attrs = {**attrs}
        book_attrs.pop('author', [])
        book_attrs.pop('language', [])
        book_attrs.pop('genre', [])

        return attrs

    @staticmethod
    def add_authors_languages_genres(instance, author_ids, language_ids, genre_ids):  # noqa C901

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
        for genre_id in genre_ids:
            genre = Genre.objects.filter(id=genre_id).first()
            # Ignore if language id in payload is invalid
            if genre:
                instance.genre.add(genre)

    @atomic
    def create(self, validated_data):
        author_ids = validated_data.pop('author', [])
        language_ids = validated_data.pop('language', [])
        genre_ids = validated_data.pop('genre', [])

        book = Book.objects.create(**validated_data)

        self.add_authors_languages_genres(book, author_ids, language_ids, genre_ids)

        return book

    @atomic
    def update(self, instance, validated_data):
        author_ids = validated_data.pop('author', [])
        language_ids = validated_data.pop('language', [])
        genre_ids = validated_data.pop('genre', [])

        instance = super().update(instance, validated_data)

        # Do not remove author references in case that payload for partial update does not contain any authors
        if author_ids:
            instance.author.remove(*instance.author.all())
        # Do not remove language references in case that payload for partial update does not contain any languages
        if language_ids:
            instance.language.remove(*instance.language.all())
        # Do not remove genre references in case that payload for partial update does not contain any genres
        if genre_ids:
            instance.genre.remove(*instance.genre.all())

        self.add_authors_languages_genres(instance, author_ids, language_ids, genre_ids)

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
            'genre',
        ]


class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True,
    )

    class Meta:
        model = BookCopy

        fields = [
            'id',
            'book',
            'book_id',
            'uid',
        ]

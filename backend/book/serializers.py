from typing import Any

from django.db.transaction import atomic
from rest_framework import serializers

from book.models import Book, BookCopy
from reference_values.models import Author, Genre, Hall, Language
from reference_values.serializers import AuthorSerializer, GenreSerializer, HallSerializer, LanguageSerializer


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    copies_count = serializers.IntegerField(read_only=True)

    def get_author(self, obj):
        authors = obj.author.order_by(
            "last_name",
            "first_name",
            "middle_name",
        )
        return AuthorSerializer(authors, many=True).data

    def get_language(self, obj):
        languages = obj.language.order_by("name")
        return LanguageSerializer(languages, many=True).data

    def get_genre(self, obj):
        genres = obj.genre.order_by("name")
        return GenreSerializer(genres, many=True).data

    class Meta:
        model = Book

        fields = (
            "id",
            "title",
            "author",
            "published_date",
            "isbn",
            "pages",
            "cover",
            "language",
            "genre",
            "copies_count",
        )


class BookCopyNestedSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)

    class Meta:
        model = BookCopy
        fields = (
            "id",
            "uid",
            "hall",
        )


class BookDetailSerializer(BookSerializer):
    copies = BookCopyNestedSerializer(
        many=True,
        read_only=True,
    )

    class Meta(BookSerializer.Meta):
        model = Book

        fields = BookSerializer.Meta.fields + ("copies",)


class BookWriteSerializer(serializers.ModelSerializer):
    author_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    language_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    genre_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        book_attrs = {**attrs}
        book_attrs.pop("author_ids", [])
        book_attrs.pop("language_ids", [])
        book_attrs.pop("genre_ids", [])

        return attrs

    @staticmethod
    def add_authors_languages_genres(
        instance: Book,
        author_ids: list[int],
        language_ids: list[int],
        genre_ids: list[int],
    ) -> None:

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
            # Ignore if genre id in payload is invalid
            if genre:
                instance.genre.add(genre)

    @atomic
    def create(self, validated_data: dict[str, Any]) -> Book:
        author_ids = validated_data.pop("author_ids", [])
        language_ids = validated_data.pop("language_ids", [])
        genre_ids = validated_data.pop("genre_ids", [])

        book = Book.objects.create(**validated_data)

        self.add_authors_languages_genres(book, author_ids, language_ids, genre_ids)

        return book

    @atomic
    def update(self, instance: Book, validated_data: dict[str, Any]) -> Book:
        author_ids = validated_data.pop("author_ids", [])
        language_ids = validated_data.pop("language_ids", [])
        genre_ids = validated_data.pop("genre_ids", [])

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

    def to_representation(self, instance: Book) -> dict[str, Any]:
        return BookSerializer(context=self.context).to_representation(instance)

    class Meta:
        model = Book

        fields = (
            "id",
            "title",
            "author_ids",
            "published_date",
            "isbn",
            "pages",
            "cover",
            "language_ids",
            "genre_ids",
        )


class BookCopyListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    hall = HallSerializer(read_only=True)

    class Meta:
        model = BookCopy
        fields = (
            "id",
            "uid",
            "book",
            "hall",
        )


class BookCopyWriteSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
    )

    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(),
        source="hall",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = BookCopy
        fields = (
            "book_id",
            "hall_id",
        )

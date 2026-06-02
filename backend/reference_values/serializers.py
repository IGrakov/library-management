from rest_framework import serializers

from reference_values.models import Author, Genre, Hall, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language

        fields = (
            "id",
            "name",
            "two_letter_code",
            "three_letter_code",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre

        fields = (
            "id",
            "name",
        )


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall

        fields = (
            "id",
            "name",
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
        )

from rest_framework import serializers

from reference_values.models import Genre, Hall, Language


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language

        fields = [
            'id',
            'name',
            'two_letter_code',
            'three_letter_code',
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre

        fields = [
            'id',
            'name',
        ]


class HallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hall

        fields = [
            'id',
            'name',
        ]

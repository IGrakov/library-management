from rest_framework import serializers

from reference_values.models import Language


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language

        fields = [
            'id',
            'name',
            'two_letter_code',
            'three_letter_code',
        ]

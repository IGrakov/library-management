import pathlib

from rest_framework import serializers

from reader_card.constants import ACCEPTED_PHOTO_FILE_EXTENSIONS
from reader_card.models import ReaderCard
from reference_values.serializers import HallSerializer
from user.serializers import UserSerializer


class ReaderCardSerializer(serializers.ModelSerializer):
    reader = UserSerializer(read_only=True)
    hall_access = HallSerializer(many=True, read_only=True)

    @staticmethod
    def validate_photo(value):
        file_extension = pathlib.Path(value).suffix.lower()
        if file_extension not in ACCEPTED_PHOTO_FILE_EXTENSIONS:
            raise serializers.ValidationError(f'File extension .{file_extension} is not allowed')
        return value

    class Meta:
        model = ReaderCard

        fields = [
            'id',
            'reader',
            'is_suspended',
            'photo',
            'hall_access',
        ]

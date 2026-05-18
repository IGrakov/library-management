import pathlib
from typing import Any

from django.core.files.uploadedfile import UploadedFile
from django.db.transaction import atomic
from rest_framework import serializers

from reader_card.constants import ACCEPTED_PHOTO_FILE_EXTENSIONS
from reader_card.models import ReaderCard
from reference_values.models import Hall
from reference_values.serializers import HallSerializer
from user.models import User
from user.serializers import UserSerializer


class ReaderCardSerializer(serializers.ModelSerializer):
    reader = UserSerializer(read_only=True)
    hall_access = HallSerializer(many=True, read_only=True)

    class Meta:
        model = ReaderCard

        fields = (
            "id",
            "reader",
            "is_suspended",
            "photo",
            "hall_access",
        )


class ReaderCardWriteSerializer(serializers.ModelSerializer):
    reader = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    hall_access = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        reader_card_attrs = {**attrs}
        reader_card_attrs.pop("reader", None)
        reader_card_attrs.pop("hall_access", [])
        return attrs

    @staticmethod
    def validate_photo(value: UploadedFile) -> UploadedFile:
        file_extension = pathlib.Path(value.name).suffix.lower()
        if file_extension.lower() not in ACCEPTED_PHOTO_FILE_EXTENSIONS:
            raise serializers.ValidationError(f"File extension {file_extension} is not allowed")  # noqa: EM102, TRY003
        return value

    @atomic
    def create(self, validated_data: dict[str, Any]) -> ReaderCard:
        hall_ids = validated_data.pop("hall_access", [])
        reader_card = ReaderCard.objects.create(**validated_data)

        for hall_id in hall_ids:
            hall = Hall.objects.filter(id=hall_id).first()
            if hall:
                reader_card.hall_access.add(hall)

        return reader_card

    @atomic
    def update(self, instance: ReaderCard, validated_data: dict[str, Any]) -> ReaderCard:
        validated_data.pop("reader", None)
        hall_ids = validated_data.pop("hall_access", [])
        instance = super().update(instance, validated_data)

        # Do not remove hall references in case that payload for partial update does not contain any halls
        if hall_ids is not None:
            instance.hall_access.clear()

        for hall_id in hall_ids:
            hall = Hall.objects.filter(id=hall_id).first()
            # Ignore if hall id in payload is invalid
            if hall:
                instance.hall_access.add(hall)

        return instance

    def to_representation(self, instance: ReaderCard) -> dict[str, Any]:
        return ReaderCardSerializer(context=self.context).to_representation(instance)

    class Meta:
        model = ReaderCard

        fields = (
            "id",
            "reader",
            "is_suspended",
            "photo",
            "hall_access",
        )

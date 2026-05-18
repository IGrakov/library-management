from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from reader_card.models import ReaderCard
from reader_card.serializers import ReaderCardSerializer, ReaderCardWriteSerializer
from user.permissions import IsLibrarian


@extend_schema_view(
    post=extend_schema(
        request=ReaderCardWriteSerializer,
        responses={
            status.HTTP_201_CREATED: ReaderCardSerializer,
        },
    ),
)
class CreateReaderCardView(generics.CreateAPIView):
    """Create new reader card"""

    parser_classes = (
        MultiPartParser,
        FormParser,
        JSONParser,
    )
    permission_classes = (IsLibrarian,)
    serializer_class = ReaderCardWriteSerializer
    queryset = ReaderCard.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve reader card by id",
    ),
    put=extend_schema(
        description="Update reader card by id",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "is_suspended": {"type": "boolean"},
                    "photo": {"type": "string", "format": "file"},
                    "hall_access": {"type": "array", "items": {"type": "integer"}},
                },
            },
            "multipart/from-data": {
                "type": "object",
                "properties": {
                    "is_suspended": {"type": "boolean"},
                    "photo": {"type": "string", "format": "uri"},
                    "hall_access": {"type": "array", "items": {"type": "integer"}},
                },
            },
        },
        responses={
            status.HTTP_200_OK: ReaderCardSerializer,
        },
    ),
    patch=extend_schema(
        description="Partially update reader card by id",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "is_suspended": {"type": "boolean"},
                    "photo": {"type": "string", "format": "file"},
                    "hall_access": {"type": "array", "items": {"type": "integer"}},
                },
            },
            "multipart/from-data": {
                "type": "object",
                "properties": {
                    "is_suspended": {"type": "boolean"},
                    "photo": {"type": "string", "format": "uri"},
                    "hall_access": {"type": "array", "items": {"type": "integer"}},
                },
            },
        },
        responses={
            status.HTTP_200_OK: ReaderCardSerializer,
        },
    ),
    delete=extend_schema(
        description="Delete reader card by id",
    ),
)
class RetrieveUpdateDeleteReaderCardView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete reader card by id"""

    parser_classes = (
        MultiPartParser,
        FormParser,
        JSONParser,
    )
    permission_classes = (IsLibrarian,)
    queryset = ReaderCard.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ReaderCardWriteSerializer
        return ReaderCardSerializer


class ListReaderCardView(generics.ListAPIView):
    """List reader cards"""

    permission_classes = (IsLibrarian,)
    queryset = ReaderCard.objects.all().select_related("reader").prefetch_related("hall_access")
    serializer_class = ReaderCardSerializer

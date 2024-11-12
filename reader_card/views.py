from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status

from reader_card.models import ReaderCard
from reader_card.serializers import ReaderCardSerializer
from user.permissions import IsLibrarian


@extend_schema_view(
    post=extend_schema(
        request=ReaderCardSerializer,
        responses={
            status.HTTP_201_CREATED: ReaderCardSerializer,
        },
    )
)
class CreateReaderCardView(generics.CreateAPIView):
    """Create new reader card"""

    permission_classes = (IsLibrarian,)
    serializer_class = ReaderCardSerializer
    queryset = ReaderCard.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve reader card by id',
    ),
    put=extend_schema(
        description='Update reader card by id',
    ),
    patch=extend_schema(
        description='Partially update reader card by id',
    ),
    delete=extend_schema(
        description='Delete reader card by id',
    ),
)
class RetrieveUpdateDeleteReaderCardView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete reader card by id"""

    permission_classes = (IsLibrarian,)
    queryset = ReaderCard.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReaderCardSerializer
        else:
            return ReaderCardSerializer


class ListReaderCardView(generics.ListAPIView):
    """List reader cards"""

    queryset = ReaderCard.objects.all().prefetch_related('reader')
    serializer_class = ReaderCardSerializer

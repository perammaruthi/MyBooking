from rest_framework import viewsets
# Create your views here.
from transport.models import Transport, Seat
from transport.serializers import TransportSerializer, SeatSerializer


class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

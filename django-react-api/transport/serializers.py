from rest_framework import serializers

from transport.models import Transport, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class TransportSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, required=False)

    class Meta:
        model = Transport
        fields = "__all__"

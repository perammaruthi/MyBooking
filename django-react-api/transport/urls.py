from rest_framework import routers

from transport.views import TransportViewSet, SeatViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register('transport', TransportViewSet, basename="transports")
router.register('seats', SeatViewSet, basename="seats")

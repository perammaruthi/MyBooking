from rest_framework import routers
from .views import MovieViewSet, RatingViewSet, UserViewSet, MovieReviewViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register('users', UserViewSet, basename="users")
router.register('movies', MovieViewSet, basename="movies")
router.register('movies/(?P<movie_id>[^/.]+)/ratings', RatingViewSet, basename="ratings")
router.register('movies/(?P<movie_id>[^/.]+)/reviews', MovieReviewViewSet, basename="reviews")

urlpatterns = router.urls

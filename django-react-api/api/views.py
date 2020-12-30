from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from api.models import Movie, Rating, Reviews, ReviewLikes
from api.serializers import MovieSerializer, RatingSerializer, UserSerializer, ReviewsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        user = request.user
        try:
            rating = Rating.objects.get(user=user.id, movie=pk)
        except ObjectDoesNotExist:
            rating = None

        data = request.data
        data["user"] = request.user.pk
        data["movie"] = pk
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {'message': 'Rating updated', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=True, url_path="avg_rating")
    def average_rating(self, request, *args, **kwargs):
        """Return average rating of a movie"""
        movie = get_object_or_404(Movie, uuid=kwargs.get("pk"))
        average_rating = movie.avg_rating
        return Response(data={"avg_rating": average_rating}, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MovieReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class ReviewLikeViewSet(viewsets.ViewSet):

    @action(methods=["POST"], detail=True, url_path="like")
    def like(self, request, *args, **kwargs):
        """
        Check if objects exists with comment pk and logged in user.
        If exists check if user already liked it and set like=False else to True
        If user disliked comment initially and now user likes it
        then change dislike to false and like to true
        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        review, exists = ReviewLikes.objects.get_or_create(
            comment_id=kwargs.get("review_id"),
            user=request.user
        )
        if exists and review.like:
            review.like = False
        else:
            review.like = True
            review.dislike = False

        review.save()
        return Response("Successfully updated")

    @action(methods=["POST"], detail=True, url_path="dislike")
    def dislike(self, request, *args, **kwargs):

        review, exists = ReviewLikes.objects.get_or_create(
            comment_id=kwargs.get("review_id"),
            user=request.user
        )
        if exists and review.dislike:
            review.dislike = False
        else:
            review.dislike = True
            review.like = False

        review.save()
        return Response("Successfully updated")

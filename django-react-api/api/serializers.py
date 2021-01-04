from rest_framework import serializers
from .models import Movie, Rating, Reviews, MovieFiles
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ReviewsSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.IntegerField(required=False)
    number_of_dislikes = serializers.IntegerField(required=False)

    class Meta:
        model = Reviews
        fields = "__all__"

    def get_number_of_likes(self, obj):
        """Return number of likes got for comment
        """
        review_likes = obj.review.all()
        return review_likes.filter(like=True).count()

    def get_number_of_dislikes(self, obj):
        """Return number of dislikes got for comment
        """
        review_likes = obj.review.all()
        return review_likes.filter(dislike=True).count()


class MovieFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFiles
        files = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    movie_files = MovieFileSerializer(many=True, required=False)
    reviews = ReviewsSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = [
            'uuid',
            'title',
            'description',
            'no_of_ratings',
            'avg_rating',
            'genre',
            'run_time',
            'release_date',
            'movie_files',
            'reviews',
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('uuid', 'stars', 'user', 'movie')

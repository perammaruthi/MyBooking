from rest_framework import serializers
from .models import Movie, Rating, Reviews
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['uuid', 'title', 'description', 'no_of_ratings', 'avg_rating']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('uuid', 'stars', 'user', 'movie')


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

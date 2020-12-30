import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UUIDMixin(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Movie(UUIDMixin):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    release_date = models.DateField(null=True, blank=True)
    # TODO make it as choice field
    genre = models.CharField(max_length=100, null=True)
    run_time = models.TimeField(null=True)
    cast = models.ManyToManyField(User, through="MovieCast", related_name="movie_cast")
    crew = models.ManyToManyField(User, through="MovieCrew", related_name="movie_crew")

    @property
    def no_of_ratings(self):
        return self.ratings.count()

    @property
    def avg_rating(self):
        rating_sum = 0
        ratings_count = self.ratings.count()
        for rating in self.ratings.all():
            rating_sum += rating.stars

        if ratings_count > 0:
            return rating_sum / ratings_count
        else:
            return 0


class Rating(UUIDMixin):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)


class MovieFiles(UUIDMixin):
    file = models.FileField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_files")


class Reviews(UUIDMixin):
    comment = models.TextField(help_text="user comment about movie")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        unique_together = (("user", "movie"), )


class MovieCast(UUIDMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_casts")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_casts")
    acted_as = models.CharField(max_length=50, help_text="User name in movie")

    class Meta:
        unique_together = (("user", "movie"), )


class MovieCrew(UUIDMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_crews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_crews")
    profession = models.CharField(max_length=50, help_text="User responsibility in movie like Producer, Writer etc..")

    class Meta:
        unique_together = (("user", "movie"), )


class ReviewLikes(UUIDMixin):
    comment = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name="review")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

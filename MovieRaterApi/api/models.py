from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=32, blank=False, null=False)
    description = models.TextField(max_length=360)

    # returns number of ratings from the 'Rating' (api_rating) table in the DB where the movie (self) appears
    def number_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            print(rating)
            sum += rating.stars

        return sum // len(ratings)


class Rating(models.Model):
    # when a movie is deleted, the rating will be deleted too
    movie = models.name = models.ForeignKey(Movie, on_delete=models.CASCADE)

    user = models.name = models.ForeignKey(User, on_delete=models.CASCADE)

    # ensures the value meets the constraints of the validators argument (between 1-5)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        # specifies that the combination of user and movie should be unique, meaning that a user can only rate a movie once.
        unique_together = ("user", "movie")

        # indicates that an index should be created for the combination of user and movie,
        # which can improve the performance of queries involving these fields.
        index_together = ("user", "movie")

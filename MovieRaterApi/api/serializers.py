from rest_framework import serializers

from api.models import Movie, Rating

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "description", "number_of_ratings", "avg_rating")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "stars", "user", "movie")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # generate toke for the user at creation. we save it in a var for possible future use.
        token = Token.objects.create(user=user)
        return user

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from api.models import Movie, Rating
from api.serializers import MovieSerializer, RatingSerializer, UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    # defines that any user can query this view set
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def rate_movie(self, request, pk=None):
        if "stars" in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data["stars"]
            user = request.user

            try:
                # if the user has a rating for the movie, update the ratings' value and save it in DB
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {"message": f"Rating updated", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                # if the user doesnt have a rating for the movie, create a new one with the 'stars' value
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {"message": f"Rating created", "result": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {"message": "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    # defines that any user can query this view set
    permission_classes = (IsAuthenticated,)

    """gets users' rating by user id

    Returns:
        _type_: _description_
    """

    @action(methods=["GET"], detail=False)
    def user_rating(self, request):
        user_rating = Rating.objects.get(user=request.user)
        print(user_rating)
        serializer = RatingSerializer(user_rating, many=False)
        response = {"message": f"{user_rating.user.id}", "result": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        response = {"message": "Your request can't be processed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {"message": "Your request can't be processed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

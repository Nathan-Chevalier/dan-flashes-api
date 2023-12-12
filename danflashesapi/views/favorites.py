from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import ShirtFavorite

class FavoriteView(ViewSet):

    def create(self, request):
        favorite = ShirtFavorite()
        favorite.shirt = request.data.get('shirt_id')
        favorite.flashes_user = request.data.get('flashes_id')
        favorite.save()

        return Response(None, status=status.HTTP_201_CREATED)
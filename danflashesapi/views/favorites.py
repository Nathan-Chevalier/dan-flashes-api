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
    
    def destroy(self, request, pk=None):
        try: 
            favorite = ShirtFavorite.objects.get(pk=pk)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except ShirtFavorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
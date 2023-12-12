from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import ShirtFavorite, Shirt, FlashesUser

class FavoriteView(ViewSet):

    def create(self, request):
        favorite = ShirtFavorite()
        pk = request.data.get('shirt_id')
        shirt = Shirt.objects.get(pk=pk)
        favorite.shirt = shirt
        favorite.flashes_user = FlashesUser.objects.get(user=request.auth.user)
        favorite.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        try: 
            favorite = ShirtFavorite.objects.get(pk=pk)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except ShirtFavorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
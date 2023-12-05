from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import FlashesUser

class FlashesUserView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            flashes_user = FlashesUser.objects.get(pk=pk)
            serialized = FlashesUserSerializer(flashes_user)
            return Response(serialized.data)

        

        except FlashesUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FlashesUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashesUser
        fields = ('id', 'flashes_name', 'profile_image_url')
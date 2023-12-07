from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import Color

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'color', 'label')

class ColorView(ViewSet):

    def list(self, request):
        colors = Color.objects.all()
        serialized = ColorSerializer(colors, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

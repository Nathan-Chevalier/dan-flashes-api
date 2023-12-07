from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import Pattern

class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'pattern_url_a', 'pattern_url_b', 'label',)

class PatternView(ViewSet):

    def list(self, request):
        patterns = Pattern.objects.all()
        serialized = PatternSerializer(patterns, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import FlashesUser, Shirt, Pattern, ShirtPattern, ShirtFavorite, Color
from django.contrib.auth.models import User

class ShirtView(ViewSet):
    def list(self, request):
        shirts = Shirt.objects.all()





class PatternSerializer:
    class Meta:
        model = Pattern
        fields = ('pattern_url_a', 'pattern_url_b', 'label',)
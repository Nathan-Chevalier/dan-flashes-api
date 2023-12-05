from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import FlashesUser, Shirt, Pattern, ShirtPattern, ShirtFavorite, Color
from django.contrib.auth.models import User

class ShirtView(ViewSet):
    def list(self, request):
        shirts = Shirt.objects.all()
        shirt_serializer = ShirtSerializer(shirts, many=True)
        return Response(shirt_serializer.data, status=status.HTTP_200_OK)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'color', 'label')

class FlashesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashesUser
        fields = ('id', 'flashes_name', 'profile_image_url')

class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'pattern_url_a', 'pattern_url_b', 'label',)

class ShirtPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShirtPattern
        fields = ('pattern','pattern_index',)

class ShirtFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShirtFavorite
        fields = ('shirt','flashes_user',)

class ShirtSerializer(serializers.ModelSerializer):
    shirt_pattern = ShirtPatternSerializer(many=True)
    flashes_user = FlashesUserSerializer(many=False)
    favorites = ShirtFavoriteSerializer(many=True)
    color = ColorSerializer(many=False)
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.flashes_user_id

    class Meta:
        model = Shirt
        fields = ('id','shirt_pattern', 'flashes_user', 'color', 'label', 'public', 'price', 'favorites', 'is_owner')
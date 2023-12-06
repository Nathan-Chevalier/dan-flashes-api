from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import FlashesUser, Shirt, Pattern, ShirtPattern, Color

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
    pattern = PatternSerializer(many=False)

    class Meta:
        model = ShirtPattern
        fields = ('pattern','pattern_index',)

class ShirtSerializer(serializers.ModelSerializer):
    shirt_pattern = ShirtPatternSerializer(many=True)
    flashes_user = FlashesUserSerializer(many=False)
    color = ColorSerializer(many=False)
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context["request"].user.id == obj.flashes_user_id

    class Meta:
        model = Shirt
        fields = ('id','shirt_pattern', 'flashes_user', 'color', 'label', 'public', 'price', 'favorites', 'is_owner')


class ShirtView(ViewSet):
    def list(self, request):
        shirts = Shirt.objects.all()

        #? Helper function to sort the shirt_pattern list of dictionaries by pattern_index in the serialized return
        def sort_pattern_by_index(pattern):
            return pattern['pattern_index']

        shirt_serializer = ShirtSerializer(shirts, many=True, context={'request':request})

        #? Uses the helper function to sort
        for shirt_data in shirt_serializer.data:
            shirt_data['shirt_pattern'] = sorted(shirt_data['shirt_pattern'], key=sort_pattern_by_index)

        return Response(shirt_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        shirt = Shirt()
        shirt.color_id = request.data.get('color')
        shirt.label = request.data.get('label')
        shirt.public = request.data.get('public')
        shirt.price = request.data.get('price')
        shirt.flashes_user = FlashesUser.objects.get(user=request.auth.user)
        shirt.save()
        patterns_data = request.data.get('patterns', [])
        pattern_ids = [pattern.get('pattern_id') for pattern in patterns_data]
        shirt.patterns.set(pattern_ids)
        for pattern in patterns_data:
            shirt_pattern = ShirtPattern.objects.get(shirt__id=shirt.id, pattern__id=pattern['pattern_id'])
            index = pattern['pattern_index']
            shirt_pattern.pattern_index.set(index)
        
        serializer = ShirtSerializer(shirt, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
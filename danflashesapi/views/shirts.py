from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from danflashesapi.models import FlashesUser, Shirt, Pattern, ShirtPattern, Color, ShirtFavorite


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'color', 'label',)

class FlashesFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShirtFavorite
        fields = ('id', 'flashes_user',)

class FlashesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashesUser
        fields = ('id', 'flashes_name', 'profile_image_url')

class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'pattern_url_a', 'pattern_url_b','pattern_preview', 'label',)

class ShirtPatternSerializer(serializers.ModelSerializer):
    pattern = PatternSerializer(many=False)

    class Meta:
        model = ShirtPattern
        fields = ('id','pattern','pattern_index',)

class ShirtSerializer(serializers.ModelSerializer):
    shirt_pattern = ShirtPatternSerializer(many=True)
    flashes_user = FlashesUserSerializer(many=False)
    color = ColorSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    shirt_favorite = FlashesFavoritesSerializer(many=True)
    price = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context["request"].user.id == obj.flashes_user_id
    
    # Returning an integer instead of a float for price
    def get_price(self, obj):
        return int(obj.price)

    class Meta:
        model = Shirt
        fields = ('id','shirt_pattern', 'flashes_user', 'color', 'label', 'public', 'price', 'shirt_favorite', 'is_owner',)

class ShirtView(ViewSet):
    def get_permissions(self):
        """
        Permission override for GET requests, does not require token
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def list(self, request):
        shirts = Shirt.objects.all()

            # Helper function to sort each instance of the pattern by its pattern index
            # Iterates through pattern dictionary and extracts the pattern index
        def sort_pattern_by_index(pattern):
            return pattern['pattern_index']

        shirt_serializer = ShirtSerializer(shirts, many=True, context={'request':request})

        #? Uses the helper function to sort via pattern index
        for shirt_data in shirt_serializer.data:
            shirt_data['shirt_pattern'] = sorted(shirt_data['shirt_pattern'], key=sort_pattern_by_index)

        return Response(shirt_serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            shirt = Shirt.objects.get(pk=pk)
        except Shirt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        def sort_pattern_by_index(pattern):
            return pattern['pattern_index']

        shirt_serializer = ShirtSerializer(shirt, many=False, context={'request':request})
        shirt_data = shirt_serializer.data
        shirt_data['shirt_pattern'] = sorted(shirt_data['shirt_pattern'], key=sort_pattern_by_index)

        return Response(shirt_data, status=status.HTTP_200_OK)
    
    def create(self, request):
        shirt = Shirt()
        shirt.color_id = request.data.get('color')
        shirt.label = request.data.get('label')
        shirt.public = request.data.get('public')
        shirt.price = request.data.get('price')
        shirt.flashes_user = FlashesUser.objects.get(user=request.auth.user)
        shirt.save()
        #? Get the patterns dictionaries
        patterns_data = request.data.get('patterns', [])

        for pattern in patterns_data:
            #? Creates ShirtPattern objects to associate Shirt, Pattern, and Pattern index
            pattern_id = pattern.get('pattern_id')
            pattern_index = pattern.get('pattern_index')
            ShirtPattern.objects.create(shirt=shirt, pattern_id=pattern_id, pattern_index=pattern_index)

        
        serializer = ShirtSerializer(shirt, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            shirt = Shirt.objects.get(pk=pk)
            shirt.color_id = request.data.get('color')
            shirt.label = request.data.get('label')
            shirt.public = request.data.get('public')
            shirt.price = request.data.get('price')
            shirt.save()
            #? Pull the join tables associated with the shirt patterns and delete them
            old_patterns = ShirtPattern.objects.filter(shirt__id=shirt.id)
            old_patterns.delete()
            #? Get the patterns dictionaries from the payload
            patterns_data = request.data.get('patterns', [])
            #? Extract the pattern_id foreign keys to associate with the shirt and set them
            pattern_ids = [pattern.get('pattern_id') for pattern in patterns_data]
            shirt.patterns.set(pattern_ids)
            #? Loop through the pattern dictionaries to pull pattern_index and associate it with the correct entry on the ShirtPattern join table.
            for pattern in patterns_data:
                shirt_pattern = ShirtPattern.objects.get(shirt__id=shirt.id, pattern__id=pattern['pattern_id'])
                index = pattern['pattern_index']
                shirt_pattern.pattern_index = index
                shirt_pattern.save()
            
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Shirt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            shirt = Shirt.objects.get(pk=pk)
            shirt.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Shirt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
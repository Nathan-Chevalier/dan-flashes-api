from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from danflashesapi.models import Shirt
from danflashesapi.views.shirts import ShirtSerializer

class MyShirtView(ViewSet):
    def list(self, request):
        user_id = request.auth.user.flashesuser.id
        shirts = Shirt.objects.filter(flashes_user=user_id)
            # Helper function to sort each instance of the pattern by its pattern index
            # Iterates through pattern dictionary and extracts the pattern index
        def sort_pattern_by_index(pattern):
            return pattern['pattern_index']

        shirt_serializer = ShirtSerializer(shirts, many=True, context={'request':request})

        #? Uses the helper function to sort via pattern index
        for shirt_data in shirt_serializer.data:
            shirt_data['shirt_pattern'] = sorted(shirt_data['shirt_pattern'], key=sort_pattern_by_index)

        return Response(shirt_serializer.data, status=status.HTTP_200_OK)
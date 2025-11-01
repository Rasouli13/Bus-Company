# home/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from travel.models import Travel
from travel.serializers import TravelSerializer  

class TravelListAPI(APIView):
    def get(self, request):
        travels = Travel.objects.all()
        serializer = TravelSerializer(travels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

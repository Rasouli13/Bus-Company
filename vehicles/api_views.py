from rest_framework import generics
from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class VehicleListAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleDetailAPIView(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

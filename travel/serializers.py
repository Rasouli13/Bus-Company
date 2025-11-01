
from rest_framework import serializers
from .models import Travel

class TravelSerializer(serializers.ModelSerializer):
    departure_city = serializers.StringRelatedField()
    arrivals_city = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Travel
        fields = ['id', 'departure_city', 'arrivals_city', 'driver', 'date', 'price', 'distance_km']

    def get_distance_km(self, obj):
        return obj.get_distance_km()

from rest_framework import serializers
from .models import Vehicle, CarCategory

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'car_type', 'capacity', 'max_speed', 'stop_time']

class VehicleSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'model_name', 'slug', 'category', 'car_type', 'capacity', 'max_speed', 'stop_time']

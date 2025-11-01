# accounts/api_serializers.py

from rest_framework import serializers
from .models import Passenger, Driver, User
from vehicles.models import Vehicle

class PassengerRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    full_name = serializers.CharField()
    national_number = serializers.CharField(min_length=10, max_length=10)
    age = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        if User.objects.filter(national_number=data['national_number']).exists():
            raise serializers.ValidationError("National number is already registered.")
        return data

    def create(self, validated_data):
        passenger, _ = Passenger.create_passenger(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            national_number=validated_data['national_number'],
            age=validated_data['age']
        )
        return passenger


class DriverRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    full_name = serializers.CharField()
    national_number = serializers.CharField(min_length=10, max_length=10)
    age = serializers.IntegerField()
    license_number = serializers.CharField(max_length=8)
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        if User.objects.filter(national_number=data['national_number']).exists():
            raise serializers.ValidationError("National number is already registered.")
        if Driver.objects.filter(license_number=data['license_number']).exists():
            raise serializers.ValidationError("License number already exists.")
        return data

    def create(self, validated_data):
        driver, _ = Driver.create_driver(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            national_number=validated_data['national_number'],
            age=validated_data['age'],
            license_number=validated_data['license_number'],
            vehicle=validated_data['vehicle']
        )
        return driver


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)

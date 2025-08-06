from django import forms
from django.shortcuts import render
from .models import Passenger,Driver
from django.core.exceptions import ValidationError
from vehicles.models import Vehicle
from travel.models import Travel


class PassengerRegistrationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField()
    national_number = forms.CharField(min_length=10, max_length=10)
    age = forms.IntegerField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if Passenger.objects.filter(user__phone_number=phone_number).exists():
            raise ValidationError("Phone number is already in use.")
        return phone_number

    def clean_national_number(self):
        national_number = self.cleaned_data.get("national_number")
        if Passenger.objects.filter(user__national_number=national_number).exists():
            raise ValidationError("National number is already in use.")
        return national_number

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('confirm_password') and cd['password'] != cd['confirm_password']:
            raise ValidationError("Passwords do not match.")
        return cd['confirm_password']


class DriverRegistrationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField()
    national_number = forms.CharField(min_length=10, max_length=10)
    age = forms.IntegerField()
    license_number = forms.CharField(max_length=8)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="Select Vehicle")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if Driver.objects.filter(user__phone_number=phone_number).exists():
            raise ValidationError("Phone number is already in use.")
        return phone_number

    def clean_national_number(self):
        national_number = self.cleaned_data.get("national_number")
        if Driver.objects.filter(user__national_number=national_number).exists():
            raise ValidationError("National number is already in use.")
        return national_number

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if Driver.objects.filter(license_number=license_number).exists():
            raise ValidationError("License number is already in use.")
        return license_number

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('confirm_password') and cd['password'] != cd['confirm_password']:
            raise ValidationError("Passwords do not match.")
        return cd['confirm_password']

    
class PassengerLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)


class DriverLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
    


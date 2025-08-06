from django.contrib import admin
from .models import Passenger, Driver,User
# Register your models here.

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'full_name', 'user_type', 'is_driver', 'is_passenger', 'is_admin')
    

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_phone_number', 'get_full_name')

    def get_phone_number(self, obj):
        return obj.user.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_phone_number', 'get_full_name', 'license_number')

    def get_phone_number(self, obj):
        return obj.user.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'




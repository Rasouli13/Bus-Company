from django.contrib import admin
from .models import Passenger, Driver,User, AdminUser
# Register your models here.

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'full_name', 'user_type', 'is_driver_icon', 'is_passenger_icon', 'is_admin')

    @admin.display(boolean=True, description='Is Driver')
    def is_driver_icon(self, obj):
        return obj.user_type == 'driver'
    
    @admin.display(boolean=True, description='Is Passenger')
    def is_passenger_icon(self, obj):
        return obj.user_type == 'passenger'

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



@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'full_name', 'is_admin_icon', 'is_driver_icon', 'is_passenger_icon')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_admin=True)

    @admin.display(boolean=True, description='Admin')
    def is_admin_icon(self, obj):
        return obj.is_admin

    @admin.display(boolean=True, description='Driver')
    def is_driver_icon(self, obj):
        return obj.is_driver

    @admin.display(boolean=True, description='Passenger')
    def is_passenger_icon(self, obj):
        return obj.is_passenger

from django.contrib import admin
from .models import Vehicle, CarCategory

class VehicleAdmin(admin.ModelAdmin):
    fields = ['model_name', 'category'] 
    list_display = ['model_name','car_type','model_name', 'max_speed', 'stop_time']

admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(CarCategory)
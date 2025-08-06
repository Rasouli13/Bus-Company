from django.contrib import admin
from .models import Travel, Ticket, CityLocation

# Register your models here.

@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'arrivals_city', 'driver', 'date', 'price')
    list_filter = ('departure_city', 'arrivals_city', 'date')
    search_fields = ('driver__user__full_name', 'departure_city__city_name', 'arrivals_city__city_name')
    filter_horizontal = ('passengers',)  # This creates a better interface for ManyToMany fields
    
    fieldsets = (
        ('Travel Information', {
            'fields': ('driver', 'departure_city', 'arrivals_city', 'date', 'price')
        }),
        ('Passengers', {
            'fields': ('passengers',),
            'description': 'Select passengers for this travel. Use the arrows to add or remove passengers.'
        }),
    )

admin.site.register(Ticket)

@admin.register(CityLocation)
class CityLocationAdmin(admin.ModelAdmin):
    list_display = ('city_name','latitude','longitude')
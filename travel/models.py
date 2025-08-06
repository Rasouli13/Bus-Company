from django.db import models
from accounts.models import Driver, Passenger
class CityLocation(models.Model):
    city_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.city_name

class Travel(models.Model):
    driver = models.ForeignKey(Driver, related_name='travels',on_delete=models.CASCADE)
    departure_city = models.ForeignKey(CityLocation, related_name='departure_city', on_delete=models.CASCADE)
    arrivals_city = models.ForeignKey(CityLocation, related_name='arrivals_city', on_delete=models.CASCADE)
    date = models.DateTimeField()
    passengers = models.ManyToManyField(Passenger, related_name='travels', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.departure_city} → {self.arrivals_city} by {self.driver.vehicle} on {self.date}"

    def get_distance_km(self):
        from math import radians, cos, sin, asin, sqrt

        lat1 = self.departure_city.latitude
        lon1 = self.departure_city.longitude
        lat2 = self.arrivals_city.latitude
        lon2 = self.arrivals_city.longitude

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # شعاع زمین به کیلومتر
        return round(c * r, 2)

    @property
    def capacity(self):
        if self.driver.vehicle:
            return self.driver.vehicle.capacity
        return 0
    
    @property
    def booked_seats(self):
        return self.tickets.count()

    @property
    def remaining_capacity(self):
        return max(0, self.capacity - self.booked_seats)
    
    @property
    def is_available(self):
        """Check if travel is available for booking"""
        from django.utils import timezone
        return (
            self.remaining_capacity > 0 and
            self.date > timezone.now() and
            self.driver.vehicle is not None
        )
    
    def get_taken_seat_numbers(self):
        """Get list of taken seat numbers"""
        return list(self.tickets.exclude(seat_number__isnull=True).values_list('seat_number', flat=True))
    
    def get_available_seat_numbers(self):
        """Get list of available seat numbers"""
        if not self.driver.vehicle:
            return []
        
        taken_seats = set(self.get_taken_seat_numbers())
        all_seats = set(range(1, self.capacity + 1))
        return sorted(list(all_seats - taken_seats))

class Ticket(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='tickets')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.PositiveIntegerField(blank=True, null=True)
    
    

    def __str__(self):
        return f"Ticket {self.id} for {self.passenger.user.full_name} on {self.travel}"

    
    


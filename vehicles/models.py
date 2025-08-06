from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import timedelta

# Create your models here.

CAR_TYPE_CHOICES = (
    ('suv', 'suv'),    
    ('van', 'van'),  
    ('bus', 'bus'),  
)
class CarCategory(models.Model):
    car_type = models.CharField(choices=CAR_TYPE_CHOICES, default='bus')
    max_speed = models.PositiveIntegerField(default=0)
    stop_time = models.DurationField(default=timedelta(minutes=15))
    capacity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.car_type

class Vehicle(models.Model):
    model_name = models.CharField(max_length=100)
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug and self.category:
            self.slug = slugify(f"{self.category.car_type}-{self.model_name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('vehicle_detail', args=[str(self.id)])
    
    @property
    def car_type(self):
        return self.category.car_type

    @property
    def max_speed(self):
        return self.category.max_speed 
    
    @property
    def capacity(self):
        return self.category.capacity
    
    @property 
    def stop_time(self):
        return self.category.stop_time
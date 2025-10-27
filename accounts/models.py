from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from vehicles.models import Vehicle
# Create your models here.

USER_TYPE_CHOICES = (
    ('driver', 'Driver'),    
    ('passenger', 'Passenger'),  
)


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    national_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField( blank=True, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone_number' # primary key
    REQUIRED_FIELDS = ['full_name']


    def __str__(self):
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.full_name

    @property
    def is_passenger(self):
        return self.user_type == 'passenger'
    
    @property
    def is_driver(self):
        return self.user_type == 'driver'

    @property
    def is_staff(self):
        return self.is_admin

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger_profile')

    @classmethod
    def create_passenger(cls, phone_number, full_name, password, national_number, age):
        user = User.objects.create_user(
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            national_number=national_number,
            age=age,
            user_type='passenger'
        )
        try:
            passenger = cls.objects.create(user=user)
            return passenger, None
        except Exception as e:
            if user in locals():
                user.delete() 
            return None, str(e) # user=None


    def __str__(self):
        return f'Passenger: {self.user.full_name}'

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=8, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def create_driver(cls, phone_number, full_name, password, national_number, age, license_number, vehicle=None):
        user = User.objects.create_user(
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            national_number=national_number,
            age=age,
            user_type='driver'
        )
        try:
            driver = cls.objects.create(
                user=user,
                license_number=license_number,
                vehicle=vehicle
            )
            return driver, None
        except Exception as e:
            if user in locals():
                user.delete() 
            return None, str(e) # user=None

    def __str__(self):
        return f'Driver: {self.user.full_name}'


class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    
    def __str__(self):
        return f'Admin: {self.full_name}'
        
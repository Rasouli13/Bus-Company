# accounts_api/urls.py

from django.urls import path
from accounts import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('passenger/register/', api_views.PassengerRegisterAPI.as_view(), name='passenger_register'),
    path('driver/register/', api_views.DriverRegisterAPI.as_view(), name='driver_register'),
    path('passenger/login/', api_views.PassengerLoginAPI.as_view(), name='passenger_login'),
    path('driver/login/', api_views.DriverLoginAPI.as_view(), name='driver_login'),
    path('logout/', api_views.LogoutAPI.as_view(), name='logout'),
]

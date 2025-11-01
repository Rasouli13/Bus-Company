from . import views
from django.urls import path

app_name = 'accounts'
passenger_urls = [
    path('passenger/login/', views.PassengerLoginView.as_view(), name='passenger_login'),
    path('passenger/register/', views.PassengerRegisterView.as_view(), name='passenger_register'),
]

driver_urls = [
    path('driver/login/', views.DriverLoginView.as_view(), name='driver_login'),
    path('driver/register/', views.DriverRegisterView.as_view(), name='driver_register'),
]

urlpatterns = passenger_urls + driver_urls + [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
]
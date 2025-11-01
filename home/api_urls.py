
from django.urls import path
from . import api_views

app_name = 'home_api'

urlpatterns = [
    path('', api_views.TravelListAPI.as_view(), name='home'),
]

from django.urls import path
from vehicles import api_views

app_name = 'vehicles_api'

urlpatterns = [
    path('', api_views.VehicleListAPIView.as_view(), name='vehicle_list_api'),
    path('<int:id>/', api_views.VehicleDetailAPIView.as_view(), name='vehicle_detail_api'),
]

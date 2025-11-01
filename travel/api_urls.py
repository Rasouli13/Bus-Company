from django.urls import path
from . import api_views

app_name = 'travel_api'

urlpatterns = [
    path('travels/', api_views.TravelListAPI.as_view(), name='travels_list'),
    path('buy_ticket/<int:travel_id>/', api_views.BuyTicketAPI.as_view(), name='buy_ticket'),
    path('my_tickets/', api_views.MyTicketsAPI.as_view(), name='my_tickets'),
    path('delete_ticket/<int:ticket_id>/', api_views.DeleteTicketAPI.as_view(), name='delete_ticket'),
    path('create_travel/', api_views.CreateTravelAPI.as_view(), name='create_travel'),
    path('my_travels/', api_views.MyTravelsAPI.as_view(), name='my_travels'),
    path('edit_travel/<int:travel_id>/', api_views.EditTravelAPI.as_view(), name='edit_travel'),
]

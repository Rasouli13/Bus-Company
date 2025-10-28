from django.urls import path
from . import views

app_name = 'travel'
urlpatterns = [
    path('buy_ticket/<int:travel_id>',views.BuyTicketView.as_view(),name='buy_ticket'),
    path('create_travel/',views.CreateTravelView.as_view(), name="create_travel"),
    path('my_tickets/', views.MyTicketsView.as_view(), name='my_tickets'),
    path('delete_ticket/<int:ticket_id>/', views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('driver-travels/', views.MyTravelsView.as_view(), name='driver_travels'),
    path('edit/<int:pk>/', views.EditTravelView.as_view(), name='edit_travel'),

]

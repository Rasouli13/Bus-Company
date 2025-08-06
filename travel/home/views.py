from django.shortcuts import render
from django.views import View
from travel.models import Travel, Ticket

# Create your views here.
class HomeView(View):
    def get(self, request):
        # Show all travels for non-authenticated users or non-passengers
        if not request.user.is_authenticated:
            travels = Travel.objects.all()
            return render(request, 'home/index.html', {'travels': travels, 'show_tickets': False})
        
        # Show user's tickets if they are a passenger
        if hasattr(request.user, 'passenger_profile'):
            tickets = Ticket.objects.filter(passenger=request.user.passenger_profile).select_related('travel', 'travel__driver', 'travel__departure_city', 'travel__arrivals_city')
            return render(request, 'home/index.html', {'tickets': tickets, 'show_tickets': True})
        
        # Show all travels for drivers or other user types
        travels = Travel.objects.all()
        return render(request, 'home/index.html', {'travels': travels, 'show_tickets': False})
   
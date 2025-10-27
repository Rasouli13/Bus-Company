from django.shortcuts import render
from django.views import View
from travel.models import Travel, Ticket

# Create your views here.
class HomeView(View):
    def get(self, request):
        # Always show available travels for all users
        travels = Travel.objects.all()
        return render(request, 'home/index.html', {'travels': travels})
   
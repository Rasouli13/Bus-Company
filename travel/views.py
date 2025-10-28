from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404
from .forms import BuyTicketForm,CreateTravelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, Travel
from .forms import EditTravelForm

# Create your views here.

class BuyTicketView(LoginRequiredMixin,View):
    form_class = BuyTicketForm
    template_name = 'travel/buy_ticket.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_passenger:
            raise Http404() 
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, travel_id):
        from django.shortcuts import get_object_or_404, render
        from .models import Travel
        
        travel = get_object_or_404(Travel, id=travel_id)
        
        # Check if travel is available for booking
        if not travel.is_available:
            from django.contrib import messages
            messages.error(request, 'This travel is not available for booking.')
            return render(request, 'travel/buy_ticket.html', {
                'travel': travel,
                'form': None,
                'error': 'This travel is not available for booking.'
            })
        
        form = self.form_class(travel=travel)
        return render(request, self.template_name, {
            'form': form,
            'travel': travel
        })
    
    def post(self, request, travel_id):
        from django.shortcuts import get_object_or_404, redirect
        from django.contrib import messages
        from .models import Travel, Ticket
        
        travel = get_object_or_404(Travel, id=travel_id)
        
        # Check if travel is still available
        if not travel.is_available:
            messages.error(request, 'This travel is not available for booking.')
            return redirect('travel:buy_ticket', travel_id=travel_id)
        
        form = self.form_class(request.POST, travel=travel)
        
        if form.is_valid():
            selected_seats = form.cleaned_data['selected_seats']
            selected_seat_numbers = [int(seat) for seat in selected_seats]
            
            # Double check if all seats are still available
            available_seats = travel.get_available_seat_numbers()
            unavailable_seats = [seat for seat in selected_seat_numbers if seat not in available_seats]
            
            if unavailable_seats:
                messages.error(request, f'These seats are no longer available: {", ".join(map(str, unavailable_seats))}')
                return redirect('travel:buy_ticket', travel_id=travel_id)
            
            # Get or create passenger profile
            from accounts.models import Passenger
            try:
                passenger = request.user.passenger_profile
            except Passenger.DoesNotExist:
                # If passenger profile doesn't exist, create one
                passenger = Passenger.objects.create(user=request.user)
            
            # Create tickets for all selected seats
            created_tickets = []
            for seat_number in selected_seat_numbers:
                ticket = Ticket.objects.create(
                    travel=travel,
                    passenger=passenger,
                    seat_number=seat_number
                )
                created_tickets.append(ticket)
                
                # Also add passenger to travel's passengers field for admin compatibility
                travel.passengers.add(passenger)
            
            # Create success message
            if len(created_tickets) == 1:
                messages.success(request, f'Your ticket has been purchased successfully. Seat number: {selected_seat_numbers[0]}')
            else:
                seat_list = ", ".join(map(str, sorted(selected_seat_numbers)))
                messages.success(request, f'Your {len(created_tickets)} tickets have been purchased successfully. Seat numbers: {seat_list}')
            
            return redirect('home:home')  # Redirect to home page
        
        return render(request, self.template_name, {
            'form': form,
            'travel': travel
        })


class MyTicketsView(LoginRequiredMixin, View):
    template_name = 'travel/my_tickets.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_passenger:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        from django.shortcuts import render
        from .models import Ticket
        
        # Get passenger profile
        try:
            passenger = request.user.passenger_profile
        except:
            from accounts.models import Passenger
            passenger = Passenger.objects.create(user=request.user)
        
        # Get all tickets for this passenger
        tickets = Ticket.objects.filter(passenger=passenger).select_related('travel', 'travel__departure_city', 'travel__arrivals_city')
        
        return render(request, self.template_name, {
            'tickets': tickets
        })


class DeleteTicketView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_passenger:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, ticket_id):
        from django.shortcuts import get_object_or_404, redirect
        from django.contrib import messages
        from .models import Ticket
        
        # Get passenger profile
        try:
            passenger = request.user.passenger_profile
        except:
            from accounts.models import Passenger
            passenger = Passenger.objects.create(user=request.user)
        
        # Get the ticket and ensure it belongs to this passenger
        ticket = get_object_or_404(Ticket, id=ticket_id, passenger=passenger)
        
        # Store ticket info for success message
        travel_info = f"{ticket.travel.departure_city} → {ticket.travel.arrivals_city}"
        seat_number = ticket.seat_number
        travel = ticket.travel
        
        # Remove passenger from travel's passengers field
        travel.passengers.remove(passenger)
        
        # Delete the ticket (this automatically frees up the seat)
        ticket.delete()
        
        messages.success(request, f'Ticket for {travel_info} (Seat {seat_number}) has been cancelled successfully.')
        return redirect('travel:my_tickets')

class CreateTravelView(LoginRequiredMixin,View):
    form_class = CreateTravelForm
    template_name = 'travel/create_travel.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_driver:
            raise Http404() 
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Travel.objects.create(
                departure_city=cd['departure_city'],
                arrivals_city=cd['arrivals_city'],
                date=cd['date'],
                price=cd['price'],
                driver=request.user.driver_profile
            )
            return redirect('home:home')
        return render(request, self.template_name, {'form':form})
            

class MyTravelsView(LoginRequiredMixin, View):
    template_name = 'travel/driver_travels.html'

    def dispatch(self, request, *args, **kwargs):
        # فقط راننده‌ها به این صفحه دسترسی دارن
        if not request.user.is_driver:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # گرفتن پروفایل راننده
        try:
            driver = request.user.driver_profile
        except:
            from accounts.models import Driver
            driver = Driver.objects.create(user=request.user)

        # گرفتن تمام سفرهای ایجاد شده توسط راننده
        travels = Travel.objects.filter(driver=driver).select_related(
            'departure_city', 'arrivals_city', 'driver__vehicle'
        ).order_by('-date')

        return render(request, self.template_name, {
            'travels': travels
        })
        
class EditTravelView(LoginRequiredMixin, View):
    template_name = 'travel/edit_travel.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_driver:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        travel = get_object_or_404(Travel, id=pk, driver=request.user.driver_profile)
        form = EditTravelForm(instance=travel)
        return render(request, self.template_name, {'form': form, 'travel': travel})

    def post(self, request, pk):
        travel = get_object_or_404(Travel, id=pk, driver=request.user.driver_profile)
        form = EditTravelForm(request.POST, instance=travel)
        if form.is_valid():
            form.save()
            return redirect('travel:driver_travels')
        return render(request, self.template_name, {'form': form, 'travel': travel})
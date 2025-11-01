from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Travel, Ticket
from .serializers import TravelSerializer
from accounts.models import Passenger, Driver
from .forms import CreateTravelForm, EditTravelForm

class TravelListAPI(APIView):
    def get(self, request):
        travels = Travel.objects.all()
        serializer = TravelSerializer(travels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyTicketAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, travel_id):
        user = request.user
        if not hasattr(user, 'passenger_profile'):
            return Response({"error": "User is not a passenger"}, status=status.HTTP_403_FORBIDDEN)

        travel = get_object_or_404(Travel, id=travel_id)
        if not travel.is_available:
            return Response({"error": "This travel is not available"}, status=status.HTTP_400_BAD_REQUEST)

        seats = request.data.get("seats", [])
        if not seats:
            return Response({"error": "No seats selected"}, status=status.HTTP_400_BAD_REQUEST)

        available_seats = travel.get_available_seat_numbers()
        unavailable = [seat for seat in seats if int(seat) not in available_seats]
        if unavailable:
            return Response({"error": f"Seats already taken: {unavailable}"}, status=status.HTTP_400_BAD_REQUEST)

        passenger = user.passenger_profile
        tickets_created = []
        for seat_number in seats:
            ticket = Ticket.objects.create(
                travel=travel,
                passenger=passenger,
                seat_number=int(seat_number)
            )
            travel.passengers.add(passenger)
            tickets_created.append({"ticket_id": ticket.id, "seat_number": seat_number})

        return Response({"success": True, "tickets": tickets_created}, status=status.HTTP_201_CREATED)

class MyTicketsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'passenger_profile'):
            return Response({"error": "User is not a passenger"}, status=status.HTTP_403_FORBIDDEN)

        passenger = user.passenger_profile
        tickets = Ticket.objects.filter(passenger=passenger).select_related(
            'travel', 'travel__departure_city', 'travel__arrivals_city'
        )
        data = []
        for t in tickets:
            data.append({
                "ticket_id": t.id,
                "travel_id": t.travel.id,
                "departure_city": str(t.travel.departure_city),
                "arrivals_city": str(t.travel.arrivals_city),
                "seat_number": t.seat_number,
                "price": t.travel.price,
                "date": t.travel.date,
                "driver": str(t.travel.driver)
            })
        return Response(data, status=status.HTTP_200_OK)

class DeleteTicketAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ticket_id):
        user = request.user
        if not hasattr(user, 'passenger_profile'):
            return Response({"error": "User is not a passenger"}, status=status.HTTP_403_FORBIDDEN)

        passenger = user.passenger_profile
        ticket = get_object_or_404(Ticket, id=ticket_id, passenger=passenger)
        travel = ticket.travel
        travel.passengers.remove(passenger)
        ticket.delete()
        return Response({"success": True, "message": f"Ticket for {travel.departure_city} → {travel.arrivals_city} deleted"}, status=status.HTTP_200_OK)

class CreateTravelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not hasattr(user, 'driver_profile'):
            return Response({"error": "User is not a driver"}, status=status.HTTP_403_FORBIDDEN)

        form = CreateTravelForm(request.data)
        if form.is_valid():
            travel = Travel.objects.create(
                departure_city=form.cleaned_data['departure_city'],
                arrivals_city=form.cleaned_data['arrivals_city'],
                date=form.cleaned_data['date'],
                price=form.cleaned_data['price'],
                driver=user.driver_profile
            )
            serializer = TravelSerializer(travel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTravelsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'driver_profile'):
            return Response({"error": "User is not a driver"}, status=status.HTTP_403_FORBIDDEN)

        travels = Travel.objects.filter(driver=user.driver_profile).select_related(
            'departure_city', 'arrivals_city', 'driver__vehicle'
        ).order_by('-date')
        serializer = TravelSerializer(travels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditTravelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, travel_id):
        user = request.user
        if not hasattr(user, 'driver_profile'):
            return Response({"error": "User is not a driver"}, status=status.HTTP_403_FORBIDDEN)

        travel = get_object_or_404(Travel, id=travel_id, driver=user.driver_profile)
        form = EditTravelForm(request.data, instance=travel)
        if form.is_valid():
            travel = form.save()
            serializer = TravelSerializer(travel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

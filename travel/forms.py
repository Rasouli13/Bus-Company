from django import forms
from django.shortcuts import render
from .models import Ticket, Travel


class BuyTicketForm(forms.Form):
    travel = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput())
    selected_seats = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        label='Select Seats',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        travel = kwargs.pop('travel', None)
        super().__init__(*args, **kwargs)
        
        if travel:
            # Set travel field
            self.fields['travel'].queryset = Travel.objects.filter(id=travel.id)
            self.fields['travel'].initial = travel
            
            # Get available seat numbers for this travel
            available_seats = travel.get_available_seat_numbers()
            
            if available_seats:
                seat_choices = [(str(seat), f'Seat {seat}') for seat in available_seats]
                self.fields['selected_seats'].choices = seat_choices
            else:
                # If no seats available, show message
                self.fields['selected_seats'].choices = []
                self.fields['selected_seats'].widget = forms.TextInput(attrs={'readonly': True})
                self.fields['selected_seats'].initial = 'No seats available'
                self.fields['selected_seats'].required = False


class CreateTravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['departure_city', 'arrivals_city', 'date', 'price']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
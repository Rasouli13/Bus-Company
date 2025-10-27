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
            self.fields['travel'].queryset = Travel.objects.filter(id=travel.id)
            self.fields['travel'].initial = travel

            available_seats = travel.get_available_seat_numbers()
            seat_choices = [(str(seat), f'Seat {seat}') for seat in available_seats]
            self.fields['selected_seats'].choices = seat_choices

    def clean_selected_seats(self):
        seats = self.cleaned_data.get('selected_seats', [])
        travel = self.cleaned_data.get('travel')
        if travel:
            available = travel.get_available_seat_numbers()
            for seat in seats:
                if int(seat) not in available:
                    raise forms.ValidationError(f"Seat {seat} is already taken.")
        return seats

class CreateTravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['departure_city', 'arrivals_city', 'date', 'price']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        

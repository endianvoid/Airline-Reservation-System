from django import forms
from .models import Flight, Reservation

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number',
            'departure_airport',
            'arrival_airport',
            'departure_time',
            'arrival_time',
            'available_seats',
            'ticket_price',
        ]


    departure_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'})
    )
    arrival_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'})
    )

class FlightReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'flight',
            'seat_count',
        ]

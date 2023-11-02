from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    departure_airport = forms.CharField(max_length=3)
    arrival_airport = forms.CharField(max_length=3)
    departure_date = forms.DateField()
    departure_time = forms.TimeField()
    passengers = forms.IntegerField()
    max_price = forms.DecimalField(max_digits=10, decimal_places=2)
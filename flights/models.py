from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Discount(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_percentage = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    min_tickets = models.PositiveIntegerField(default=1)
    min_flights = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_airport = models.CharField(max_length=3)
    arrival_airport = models.CharField(max_length=3)
    available_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def arrival_time_must_be_after_departure_time(self):
        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    passport_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    frequent_flyer_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    seat_number = models.CharField(max_length=5)
    is_paid = models.BooleanField(default=False)
    family_members = models.ManyToManyField(FamilyMember, blank=True)

    def __str__(self):
        return f"Reservation for {self.passenger.username} on {self.flight.flight_number}"

phone_regex = RegexValidator(
    regex=r'^[0-9-]*$',
    message='Phone number can only contain digits and hyphens.'
)


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Payment for Reservation {self.reservation.id}"

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=50)
    seating_capacity = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.manufacturer} {self.aircraft_type}"

class AirportConnection(models.Model):
    source_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='source_connections')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_connections')
    connecting_flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        return f"Connection from {self.source_airport} to {self.destination_airport}"
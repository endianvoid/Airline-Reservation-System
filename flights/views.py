from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, AirportConnection, Discount, Reservation, Payment
from django.shortcuts import render, redirect
from .models import Flight
from .forms import FlightForm, FlightReserveForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from datetime import datetime

@login_required
def user_profile(request):
    user = request.user
    reservations = Reservation.objects.filter(passenger=user)
    total_tickets_purchased = reservations.count()
    context = {
        'user': user,
        'reservations': reservations,
        'total_tickets_purchased': total_tickets_purchased,
    }

    return render(request, 'user_profile.html', context)

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect("/")

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, 'flight_detail.html',  {'flight': flight})

def reservation_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'reservation_details.html', {'reservation': reservation})

def payment_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'payment.html')


def search_view(request):
    query = request.GET.get('q')

    if query:
        flights = Flight.objects.filter(
            Q(flight_number__icontains=query) |
            Q(departure_airport__icontains=query) |
            Q(arrival_airport__icontains=query)
        )
    else:
        flights = Flight.objects.all()

    return render(request, 'search.html', {'flights': flights})

@login_required
def calculate_discount(request):
    user = request.user
    reservations = Reservation.objects.filter(passenger=user)
    flights = Flight.objects.filter(reservation__in=reservations)

    applicable_discounts = []

    for discount in Discount.objects.all():
        if (
            len(reservations) >= discount.min_tickets
            and len(flights.filter(flight_number__in=discount)) >= discount.min_flights
        ):
            applicable_discounts.append(discount)

    context = {'user': user, 'applicable_discounts': applicable_discounts}
    return render(request, 'discounts.html', context)

def find_connecting_flights(request):
    if request.method == 'POST':
        departure_airport = request.POST.get('departure_airport')
        arrival_airport = request.POST.get('arrival_airport')

        connections = AirportConnection.objects.filter(
            source_airport=departure_airport,
            destination_airport=arrival_airport,
        )

        context = {'connections': connections}
        return render(request, 'connecting_flights.html', context)
    else:
        return render(request, 'select_airports.html')



@login_required
def create_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flight_list')
    else:
        form = FlightForm()

    return render(request, 'create_flight.html', {'form': form})

@login_required
def reserve_flight(request):
    if request.method == 'POST':
        form = FlightReserveForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.reservation_date = datetime.now()
            reservation.passenger = request.user

            if reservation.flight.available_seats < reservation.seat_count:
                return redirect('reserve_flight')
            else:
                #reservation.flight.available_seats = reservation.flight.available_seats - reservation.seat_count
                #reservation.flight.save()
                #reservation.save()
                request.session['flight_reservation_detail'] = request.POST
                request.session['flight_reservation_object_id'] = reservation.flight.pk
                return redirect('payment_page')
    else:
        form = FlightReserveForm()

        return render(request, 'reserve_flight.html', {'form': form})

@login_required
def update_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)

    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('flight_list')
    else:
        form = FlightForm(instance=flight)

    return render(request, 'update_flight.html', {'form': form})

@login_required
def delete_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)

    if request.method == 'POST':
        flight.delete()
        return redirect('flight_list')

    return render(request, 'delete_flight.html')


def flight_list(request):
    flights = Flight.objects.all()
    context={

      'flights':flights
    }
    return render(request, 'flight_list.html', context)


def landing_page(request):
    return render(request, 'BaseLanding.html')

def payment_page(request):
    if request.method == 'POST':
        form = FlightReserveForm(request.session['flight_reservation_detail'])
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.reservation_date = datetime.now()
            reservation.passenger = request.user

            if reservation.flight.available_seats < reservation.seat_count:
                return redirect('reserve_flight')
            else:
                reservation.flight.available_seats = reservation.flight.available_seats - reservation.seat_count
                reservation.flight.save()
                reservation.save()
                return redirect('payment_thank_you')
    else:
        flight = Flight.objects.get(pk=request.session['flight_reservation_object_id'])
        return render(request, "payment_page.html", {"flight" : flight})

def payment_thanks(request):
    return render(request, "payment_thankyou.html")

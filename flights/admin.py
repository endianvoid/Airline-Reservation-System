from django.contrib import admin

# Register your models here.
from .models import Flight, Reservation
admin.site.register(Flight)
admin.site.register(Reservation)
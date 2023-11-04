"""
URL configuration for AirlineReservationSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flights import views
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.urls import include
from flights.views import landing_page
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('flight_list/', views.flight_list, name='flight_list'),
    path('registration_view/', views.registration_view, name='registration_view'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('login_view/', views.login_view, name='login_view'),
    path('flight_detail/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('payment_view/', views.payment_view, name='payment_view'),
    path('search_view/', views.search_view, name='search_view'),
    path('calculate_discount/', views.calculate_discount, name='calculate_discount'),
    path('find_connecting_flights/', views.find_connecting_flights, name='find_connecting_flights'),
    path('create_flight/', views.create_flight, name='create_flight'),
    path('update_flight/<int:flight_id>/', views.update_flight, name='update_flight'),
    path('delete_flight/<int:flight_id>/', views.delete_flight, name='delete_flight'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
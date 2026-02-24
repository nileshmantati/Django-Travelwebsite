from django.contrib import admin
from .models import Airline, FlightModel, FlightClass, FlightBooking

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(FlightModel)
class FlightModelAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'source', 'destination', 'departure_time', 'is_active')
    list_filter = ('airline', 'source', 'destination', 'is_active')
    search_fields = ('flight_number', 'airline__name')

@admin.register(FlightClass)
class FlightClassAdmin(admin.ModelAdmin):
    list_display = ('flight', 'class_type', 'available_seats', 'total_seats', 'base_price')
    list_editable = ('available_seats', 'base_price')

@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'flight', 'passenger_name','passport_number', 'booking_status', 'booked_at')
    readonly_fields = ('booking_id', 'booked_at')
    search_fields = ('booking_id', 'passenger_name', 'user__username')
from django.contrib import admin
from .models import BusModel,City,BusBooking

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number','bus_name','bus_type','bus_seating_type','total_seats','available_seats','source','destination','departure_time','arrival_time','price','is_active')
    list_filter = ('bus_type', 'bus_seating_type', 'is_active')
    search_fields = ('bus_name', 'bus_number')
    
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
class BusBookingAdmin(admin.ModelAdmin):
    list_display = ('user','bus','seat_number','travel_date','price','booking_status','payment_status','booked_at')
    search_fields = ('name',)
    
admin.site.register(City,CityAdmin)
admin.site.register(BusModel,BusAdmin)
admin.site.register(BusBooking,BusBookingAdmin)
    
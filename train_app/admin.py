from django.contrib import admin
from .models import TrainModel, TrainBooking, TrainCoach

class TrainAdmin(admin.ModelAdmin):
    list_display = (
        'train_number', 'train_name', 'source', 'destination', 
        'travel_date', 'departure_time', 'arrival_time', 'is_active'
    )
    list_filter = ('is_active', 'travel_date', 'source')
    search_fields = ('train_name', 'train_number')

class TrainCoachAdmin(admin.ModelAdmin):
    list_display = ('train', 'coach_type', 'total_seats', 'available_seats', 'price')
    list_filter = ('coach_type', 'train')
    search_fields = ('train__train_name', 'coach_type')

class TrainBookingAdmin(admin.ModelAdmin):
    list_display = (
        'pnr_number', 'user', 'train', 'coach', 
        'passenger_name', 'booking_status', 'booked_at'
    )
    list_filter = ('booking_status', 'booked_at')
    search_fields = ('pnr_number', 'passenger_name', 'user__username')
    readonly_fields = ('pnr_number',)

# Registering models
admin.site.register(TrainModel, TrainAdmin)
admin.site.register(TrainCoach, TrainCoachAdmin)
admin.site.register(TrainBooking, TrainBookingAdmin)
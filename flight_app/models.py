from django.db import models
from bus_app.models import City
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from django.db.models import F

# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True)
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class FlightModel(models.Model):
    flight_number = models.CharField(max_length=30, unique=True)
    source = models.ForeignKey(City, on_delete=models.CASCADE, related_name="flight_source")
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="flight_destination")
    
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    travel_date = models.DateField()
    
    # Flight specific details
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="flights")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.airline.name} - {self.flight_number}"
    
    def clean(self):
        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time.")
    
class FlightClass(models.Model):
    CLASS_CHOICES = [
        ('ECONOMY', 'Economy'),
        ('PREMIUM_ECONY', 'Premium Economy'),
        ('BUSINESS', 'Business'),
        ('FIRST_CLASS', 'First Class'),
    ]
    flight = models.ForeignKey(FlightModel, on_delete=models.CASCADE, related_name="classes")
    class_type = models.CharField(max_length=30, choices=CLASS_CHOICES)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Flight specific features
    baggage_check_in = models.CharField(max_length=50, default="15 KG")
    baggage_cabin = models.CharField(max_length=50, default="7 KG")
    
    class Meta:
        unique_together = ('flight', 'class_type') # Prevents duplicate classes for one flight

    def __str__(self):
        return f"{self.flight.flight_number} - {self.class_type}"
    
class FlightBooking(models.Model):
    BOOKING_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )
    booking_id = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(FlightModel, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE)
    
    passenger_name = models.CharField(max_length=100)
    passenger_age = models.PositiveIntegerField()
    passenger_gender = models.CharField(
        max_length=10,
        choices=(('Male','Male'), ('Female','Female'), ('Other','Other')),
        null=True,
        blank=True
    )
    passport_number = models.CharField(max_length=20, null=True, blank=True) # International flights ke liye
    
    seat_number = models.CharField(max_length=30, blank=True)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_status = models.CharField(max_length=20,choices=BOOKING_STATUS, default='PENDING')
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS, default='PENDING')
    booked_at = models.DateTimeField(auto_now_add=True)

    def cancel(self):
        if self.booking_status == 'CANCELLED':
            return
        with transaction.atomic():
            # Use F() expression to prevent race conditions during cancellation
            FlightClass.objects.filter(id=self.flight_class.id).update(available_seats=F('available_seats') + 1)
            self.flight_class.save()
            
            self.booking_status = 'CANCELLED'
            self.payment_status = 'CANCELLED'
            self.save()
            
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = str(uuid.uuid4().hex[:10].upper())
        
        # Atomic transaction for seat management
        if not self._state.adding:
            with transaction.atomic():
                selected_class = FlightClass.objects.select_for_update().get(id=self.flight_class.id)
                if selected_class.available_seats > 0:
                    selected_class.available_seats -= 1
                    selected_class.save()
                    self.price_at_booking = selected_class.base_price
                else:
                    raise ValueError("Sorry, no seats available in this class!")
        
        super().save(*args, **kwargs)
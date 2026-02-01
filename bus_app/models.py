from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError,ObjectDoesNotExist
# from travel.models import Registration
# from django.contrib.auth.models import User
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100,unique=True)
    image = models.ImageField(upload_to="cities/")

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    
class BusModel(models.Model):
    BUS_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('NON-AC', 'Non AC'),
    ]
    BUS_SEATING_TYPE_CHOICES = [
        ('SLEEPER', 'Sleeper'),
        ('SEATER', 'Seater'),
    ]
    bus_number = models.CharField(max_length=20)
    bus_name = models.CharField(max_length=50)
    bus_type = models.CharField(
        max_length=20,
        choices=BUS_TYPE_CHOICES,
    )
    bus_seating_type = models.CharField(
        max_length=20,
        choices=BUS_SEATING_TYPE_CHOICES,
        null=True, blank=True
    )
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    source = models.ForeignKey(City, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destination_routes")
    travel_date = models.DateField(default=timezone.localdate)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    rating = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    price = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus_name} ({self.bus_number})"
    
    def is_available(self):
        return self.is_active and self.available_seats > 0
    
    def clean(self):
        # Check for seats comparison
        if self.available_seats is not None and self.total_seats is not None:
            if self.available_seats > self.total_seats:
                raise ValidationError("Available seats cannot be greater than total seats")

        # Check for time comparison (Yahan error aa rahi thi)
        if self.arrival_time and self.departure_time:
            if self.arrival_time <= self.departure_time:
                raise ValidationError("Arrival time must be after departure time")

        src = getattr(self, 'source', None)
        dest = getattr(self, 'destination', None)
        # self.source access karne par agar object nahi mila toh RelatedObjectDoesNotExist trigger hoga
        if src and dest:
            if src == dest:
                raise ValidationError("Source and destination cannot be the same")
            
    class Meta:
        ordering = ['travel_date', 'departure_time']
        indexes = [
            models.Index(fields=['source', 'destination', 'travel_date']),
        ]
        unique_together = (
            "bus_number",
            "source",
            "destination",
            "travel_date",
            "departure_time",
        )


class BusBooking(models.Model):
    BOOKING_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='bookings')
    bus = models.ForeignKey(BusModel,on_delete=models.CASCADE)
    travel_date = models.DateField()
    seat_number = models.CharField(max_length=10,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    passenger_name = models.CharField(max_length=100,default="Guest")
    passenger_age = models.PositiveIntegerField(default=18)
    passenger_gender = models.CharField(
        max_length=10,
        choices=(('Male','Male'), ('Female','Female'), ('Other','Other')),
        null=True,
        blank=True
    )
    passenger_phone = models.CharField(max_length=15,null=True,
        blank=True)
    booking_status = models.CharField(max_length=20,
        choices=BOOKING_STATUS,
        default='PENDING')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING')
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    
    def cancel(self):
        if self.booking_status != 'CANCELLED':
            self.booking_status = 'CANCELLED'
            self.bus.available_seats += 1  # Restore seat
            self.bus.save()
            self.save()
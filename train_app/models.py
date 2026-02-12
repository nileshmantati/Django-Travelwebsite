from django.db import models
from django.conf import settings
from bus_app.models import City
from django.db import transaction

class TrainModel(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    train_name = models.CharField(max_length=100)
    source = models.ForeignKey(City, on_delete=models.CASCADE, related_name="train_source")
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="train_destination")
    
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    travel_date = models.DateField()
    
    # Train specific details
    runs_on = models.CharField(max_length=50, help_text="Example: Mon, Wed, Fri")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.train_name} ({self.train_number})"

class TrainCoach(models.Model):
    COACH_CHOICES = [
        ('1AC', 'First Class AC'),
        ('2AC', 'Second Class AC'),
        ('3AC', 'Third Class AC'),
        ('SL', 'Sleeper'),
        ('2S', 'Second Sitting'),
    ]
    train = models.ForeignKey(TrainModel, on_delete=models.CASCADE, related_name="coaches")
    coach_type = models.CharField(max_length=10, choices=COACH_CHOICES)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.train.train_name} - {self.coach_type}"

class TrainBooking(models.Model):
    pnr_number = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    train = models.ForeignKey(TrainModel, on_delete=models.CASCADE)
    coach = models.ForeignKey(TrainCoach, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    passenger_age = models.PositiveIntegerField()
    passenger_gender = models.CharField(
        max_length=10,
        choices=(('Male','Male'), ('Female','Female'), ('Other','Other')),
        null=True,
        blank=True
    )
    seat_number = models.CharField(max_length=10)
    booking_status = models.CharField(max_length=20, default='CONFIRMED')
    booked_at = models.DateTimeField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        if not self.pnr_number:
            import uuid
            self.pnr_number = str(uuid.uuid4().hex[:10].upper())
        
        # Seat minus karne ka logic
        if not self.pk:  # Sirf tab jab nayi booking create ho rahi ho
            with transaction.atomic():
                coach = self.coach
                if coach.available_seats > 0:
                    coach.available_seats -= 1
                    coach.save()
                else:
                    raise ValueError("No seats available in this coach!")
        
        super().save(*args, **kwargs)
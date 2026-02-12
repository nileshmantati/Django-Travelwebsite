from .models import TrainModel, TrainCoach, City
from datetime import datetime, timedelta
from django.utils import timezone
# ... baaki imports wahi rahenge ...

def insert_weekly_data():
    today = timezone.localdate()
    # Purani trains inactive karna
    TrainModel.objects.filter(travel_date__lt=today, is_active=True).update(is_active=False)

    routes = [
        ("Delhi", "Mumbai"),
        ("Mumbai", "Pune"),
        ("Pune", "Delhi"),
    ]

    # Train ki general details
    train_data = [
        {
            "train_name": "Rajdhani Express",
            "train_number": "12432",
            "runs_on": "Daily",
            "departure_time": "16:30",
            "arrival_time": "08:30",
            "coaches": [
                {"type": "1AC", "price": 4500, "seats": 20},
                {"type": "2AC", "price": 3200, "seats": 40},
                {"type": "3AC", "price": 2200, "seats": 60},
            ]
        },
        {
            "train_name": "Garib Rath",
            "train_number": "12910",
            "runs_on": "Mon, Wed, Fri",
            "departure_time": "12:00",
            "arrival_time": "04:00",
            "coaches": [
                {"type": "3AC", "price": 1100, "seats": 70},
                {"type": "SL", "price": 500, "seats": 80},
            ]
        }
    ]

    for day in range(7):
        travel_date = today + timedelta(days=day)

        for source_name, destination_name in routes:
            try:
                source = City.objects.get(name=source_name)
                destination = City.objects.get(name=destination_name)
            except City.DoesNotExist:
                continue

            for data in train_data:
                # Dynamic train number for uniqueness across dates (Optional)
                # Agar aap unique_together constraint use kar rahe ho to ye zaroori hai
                unique_number = f"{data['train_number']}-{travel_date.strftime('%d%m')}"

                dep_time = timezone.make_aware(
                    datetime.combine(travel_date, datetime.strptime(data["departure_time"], "%H:%M").time())
                )
                arr_time = dep_time + timedelta(hours=16) # Example duration

                # 1. Train Create karein
                train, created = TrainModel.objects.get_or_create(
                    train_number=unique_number,
                    travel_date=travel_date,
                    defaults={
                        'train_name': data["train_name"],
                        'source': source,
                        'destination': destination,
                        'departure_time': dep_time,
                        'arrival_time': arr_time,
                        'runs_on': data["runs_on"],
                        'is_active': True
                    }
                )

                # 2. Train ke Coaches Create karein (Agar train abhi bani hai)
                if created:
                    for coach in data["coaches"]:
                        TrainCoach.objects.create(
                            train=train,
                            coach_type=coach["type"],
                            total_seats=coach["seats"],
                            available_seats=coach["seats"],
                            price=coach["price"]
                        )

    print("Weekly Train data inserted successfully!")
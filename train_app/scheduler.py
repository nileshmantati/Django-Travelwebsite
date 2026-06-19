from .models import TrainModel, TrainCoach, City
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.utils import timezone

def insert_weekly_train_data():
    today = timezone.localdate()
    TrainModel.objects.filter(travel_date__lt=today, is_active=True).update(is_active=False)

    routes = [
        ("Delhi","Mumbai"),
        ("Mumbai", "Pune"),
        ("Pune", "Delhi"),
        ("Mumbai","Delhi"),
        ("Pune","Mumbai"),
        ("Delhi","Pune"),
    ]
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
                 # Current day name (Mon, Tue, Wed...)
                current_day = travel_date.strftime("%a")
                 # Daily train hai to har din chalegi
                if data["runs_on"] != "Daily":

                    allowed_days = [
                        day.strip()
                        for day in data["runs_on"].split(",")
                    ]

                    if current_day not in allowed_days:
                        continue
                # Dynamic train number for uniqueness across dates (Optional)
                # Agar aap unique_together constraint use kar rahe ho to ye zaroori hai
                unique_number = f"{data['train_number']}-{source.id}-{destination.id}-{travel_date.strftime('%d%m')}"

                dep_time = timezone.make_aware(
                    datetime.combine(travel_date, datetime.strptime(data["departure_time"], "%H:%M").time())
                )
                arr_time = timezone.make_aware(
                    datetime.combine(
                        travel_date + timedelta(days=1),  # next day arrival
                        datetime.strptime(data["arrival_time"], "%H:%M").time()
                    )
                )

                # 1. Train Create karein
                train, created = TrainModel.objects.get_or_create(
                    train_number=unique_number,
                    travel_date=travel_date,
                    source=source,
                    destination=destination,
                    defaults={
                        'train_name': data["train_name"],
                        'departure_time': dep_time,
                        'arrival_time': arr_time,
                        'runs_on': data["runs_on"],
                        'is_active': True
                    }
                )

                # 2. Train ke Coaches Create karein (Agar train abhi bani hai)
                if created:
                    for coach in data["coaches"]:
                        TrainCoach.objects.get_or_create(
                        train=train,
                        coach_type=coach["type"],
                        defaults={
                            "total_seats": coach["seats"],
                            "available_seats": coach["seats"],
                            "price": coach["price"]
                        }
                    )

    print("Weekly Train data inserted successfully!")
    
def start():
    scheduler = BackgroundScheduler()
    
    # Every Sunday at 1:00 AM
    # scheduler.add_job(
    #     insert_weekly_train_data,
    #     trigger='cron',
    #     day_of_week='sun',
    #     hour=1,
    #     minute=0
    # )
    scheduler.add_job(
        insert_weekly_train_data,
        trigger='interval',
        minutes=2
    )
    print("Train Scheduler Started")
    # scheduler.add_job(insert_weekly_train_data)  # Run every 24 hours
    scheduler.start()


from bus_app.models import City
from .models import FlightModel, Airline, FlightClass
from datetime import datetime, timedelta
from django.utils import timezone

def insert_weekly_data():
    today = timezone.localdate()
    FlightModel.objects.filter(travel_date__lt=today, is_active=True).update(is_active=False)

    routes = [
        ("Delhi","Mumbai"),
        ("Mumbai", "Pune"),
        ("Pune", "Delhi"),
        ("Mumbai","Delhi"),
        ("Pune","Mumbai"),
        ("Delhi","Pune"),
    ]
    
    indigo, _ = Airline.objects.get_or_create(name="IndiGo", code="6E")
    air_india, _ = Airline.objects.get_or_create(name="Air India", code="AI")
    
    flight_data = [
        {
            "airline": indigo,
            "flight_no_prefix": "6E-501",
            "departure_time": "08:00",
            "duration_hours": 2,
            "classes": [
                {"type": "ECONOMY", "price": 4500, "seats": 120},
                {"type": "PREMIUM_ECONY", "price": 6500, "seats": 20},
            ]
        },
        {
            "airline": air_india,
            "flight_no_prefix": "AI-802",
            "departure_time": "14:30",
            "duration_hours": 2.5,
            "classes": [
                {"type": "ECONOMY", "price": 5000, "seats": 100},
                {"type": "BUSINESS", "price": 15000, "seats": 12},
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
                print(f"City {source_name} or {destination_name} not found.")
                continue

            for data in flight_data:
                # Create a unique flight number for each date and route
                # Format: 6E-501-DELBOM-1602 (FlightNo-Route-DayMonth)
                unique_number = f"{data['flight_no_prefix']}-{source.id}{destination.id}-{travel_date.strftime('%d%m')}"

                dep_time = timezone.make_aware(
                    datetime.combine(travel_date, datetime.strptime(data["departure_time"], "%H:%M").time())
                )
                arr_time = dep_time + timedelta(hours=data["duration_hours"])

                # 1. Flight Create karein
                flight, created = FlightModel.objects.get_or_create(
                    flight_number=unique_number,
                    defaults={
                        'airline': data["airline"],
                        'source': source,
                        'destination': destination,
                        'departure_time': dep_time,
                        'arrival_time': arr_time,
                        'travel_date': travel_date,
                        'is_active': True
                    }
                )

                # 2. Flight ke Classes Create karein (Agar Flight abhi bani hai)
                if created:
                    for f_class in data["classes"]:
                        FlightClass.objects.create(
                            flight=flight,
                            class_type=f_class["type"],
                            total_seats=f_class["seats"],
                            available_seats=f_class["seats"],
                            base_price=f_class["price"]
                        )

    print("Weekly Flight data inserted successfully!")
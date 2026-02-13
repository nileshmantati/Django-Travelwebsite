from django.utils import timezone
from .models import BusModel,City
from datetime import datetime, timedelta
import random,string

def insert_weekly_data():
    today = timezone.localdate()
    BusModel.objects.filter(travel_date__lt=today, is_active=True).update(is_active=False)
    
    routes = [
        ("Delhi","Mumbai"),
        ("Mumbai", "Pune"),
        ("Pune", "Delhi"),
        ("Mumbai","Delhi"),
        ("Pune","Mumbai"),
        ("Delhi","Pune"),
    ]
    buses = [
        {
            "base_name": "SHREE",
            "bus_name": "Shree Travels",
            "bus_type": "AC",
            "bus_seating_type": "SLEEPER",
            "total_seats": 40,
            "available_seats": 40,
            "departure_time": "22:00",
            "arrival_time": "06:00",
            "price": 1500,
            "rating":4.2,
        },
        {
            "base_name": "EAGLE",
            "bus_name": "Eagle Express",
            "bus_type": "NON-AC",
            "bus_seating_type": "SEATER",
            "total_seats": 45,
            "available_seats": 45,
            "departure_time": "20:00",
            "arrival_time": "05:30",
            "price": 900,
            "rating":3.5,
        }
    ]
    for day in range(7):
        travel_date = today + timedelta(days=day)
        
        for source_name, destination_name in routes:
                source = City.objects.get(name=source_name)
                destination = City.objects.get(name=destination_name)
                for bus in buses:
                    dep_time = timezone.make_aware(
                        datetime.combine(
                            travel_date,
                            datetime.strptime(bus["departure_time"], "%H:%M").time()
                        )
                    )
                    
                    number = random.randint(1000, 9999)
                    alphabet = random.choice(string.ascii_uppercase)
                    unique_bus_number = f'{"MH"}{source.id}{destination.id}{alphabet}{alphabet}{number}'
                    if BusModel.objects.filter(
                        bus_number=unique_bus_number,
                        bus_name=bus["bus_name"],
                        source=source,
                        destination=destination,
                        departure_time=dep_time,
                        travel_date=travel_date
                    ).exists():
                        continue  

                    arr_time = timezone.make_aware(
                        datetime.combine(
                            travel_date + timedelta(days=1),
                            datetime.strptime(bus["arrival_time"], "%H:%M").time()
                        )
                    )

                    BusModel.objects.create(
                        bus_number=unique_bus_number,
                        bus_name=bus["bus_name"],
                        bus_type=bus["bus_type"],
                        bus_seating_type=bus["bus_seating_type"],
                        total_seats=bus["total_seats"],
                        available_seats=bus["available_seats"],
                        source=source,
                        destination=destination,
                        travel_date=travel_date,
                        departure_time=dep_time,
                        arrival_time=arr_time,
                        rating=bus["rating"],
                        price=bus["price"],
                        is_active=True
                    )

    print("Sunday midnight data inserted")


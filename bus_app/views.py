from django.shortcuts import render,redirect,get_object_or_404
from .models import BusModel
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib import messages
from .models import BusBooking
from django.contrib.auth.decorators import login_required
from .forms import PassengerForm
from django.core.paginator import Paginator


def bus_search(request):
    buses = BusModel.objects.none()
    bus_list = []
    
    from_city = request.GET.get('from', '').strip()
    to_city = request.GET.get('to', '').strip()
    price = request.GET.get('price')
    rating = request.GET.get('rating')
    bus_type = request.GET.get('bus_type')
    seat_type = request.GET.get('seat_type')
    
    if request.GET.get('today'):
        travel_date = now().date()
    elif request.GET.get('tomorrow'):
        travel_date = now().date() + timedelta(days=1)
    else:
        date_str = request.GET.get('date')
        travel_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    if from_city and to_city:
        if from_city.lower() == to_city.lower():
            messages.error(request, "From and To cities cannot be the same")
            return redirect('home')
        
        history = request.session.get('search_history', [])
        
        new_search = {
            'from': from_city,
            'to': to_city,
            'date': str(travel_date or now().date()),
            'searched_at': now().isoformat()
        }
        history = [h for h in history if h != new_search]
        history.insert(0, new_search)
        request.session['search_history'] = history[:5]
        
        buses = BusModel.objects.filter(
            source__name__icontains=from_city,
            destination__name__icontains=to_city,
            is_active=True
        )
        if travel_date:
            buses = buses.filter(travel_date=travel_date)
            
        if price:
            if price == '0-500':
                buses = buses.filter(price__lt=500)
            elif price == '500-1000':
                buses = buses.filter(price__gte=500, price__lte=1000)
            elif price == '1000+':
                buses = buses.filter(price__gt=1000)

        if rating:
            buses = buses.filter(rating__gte=rating)

        if bus_type:
            buses = buses.filter(bus_type=bus_type)

        if seat_type:
            buses = buses.filter(bus_seating_type=seat_type)
            
        for bus in buses:
            dep = bus.departure_time
            arr = bus.arrival_time
            if arr < dep: 
                arr += timedelta(days=1)

            duration = arr - dep
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60

            bus_list.append({
                'bus': bus,
                'duration': f"{hours}h {minutes}m"
            })
        buses = BusModel.objects.all()
        paginator = Paginator(bus_list, 5) # Show 5 buses per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'from_city': from_city,
            'to_city': to_city,
            'travel_date': travel_date or now().date(),
            'page_obj': page_obj,
        }
        return render(request, 'all_bus.html', context)
    
    messages.error(request, "Please enter both From and To cities")
    return redirect('home')

@login_required(login_url='login')
def my_bus_booking(request):
    bookings = BusBooking.objects.filter(user=request.user)
    return render(request,'my_bus_booking.html',{'bookings': bookings})

@login_required(login_url='login')
def cancel_booking(request, pk):
    booking = get_object_or_404(BusBooking, pk=pk, user=request.user)
    
    if booking.booking_status == 'CANCELLED':
        messages.info(request, "Booking already cancelled.")
    else:
        booking.cancel()
        booking.delete()
        messages.success(request, "Booking cancelled and seat restored.")

    return redirect('my_bus_booking')

# For Seater Bus
def generate_seats_for_seater(total_seats=50):
    columns = []
    seats_per_column = 5

    seat_no = 1

    while seat_no <= total_seats:
        col = []
        for _ in range(seats_per_column):
            if seat_no <= total_seats:
                col.append(f"S{seat_no}")
                seat_no += 1
        columns.append(col[::-1])

    return columns

def generate_seats_for_sleeper(seat_type="L",total_seats=50):
    columns = []
    seats_per_column = 3
    seat_no = 1

    while seat_no <= total_seats:
        col = []
        for _ in range(seats_per_column):
            if seat_no <= total_seats:
                col.append(f"{seat_type}{seat_no}")
                seat_no += 1
        columns.append(col[::-1])
        
    return columns

@login_required(login_url='login')
def bus_seat_view(request, pk):
    bus = get_object_or_404(BusModel, pk=pk)

    booked_seats = BusBooking.objects.filter(
        bus=bus,
        travel_date=bus.travel_date,
        booking_status='Pending'
    ).values_list('seat_number', flat=True)

    if bus.bus_seating_type == 'SLEEPER':
        seats_layout_upper = generate_seats_for_sleeper("U", bus.total_seats // 2)
        seats_layout_lower = generate_seats_for_sleeper("L", bus.total_seats // 2)
    else:
        seats_layout = generate_seats_for_seater(bus.total_seats)
    
    if request.method == "POST":
        selected_seat = request.POST.get('seat')

        if not selected_seat:
            messages.error(request, "Please select a seat")
            return redirect(request.path)

        if selected_seat in booked_seats:
            messages.error(request, "Seat already booked")
            return redirect(request.path)

        # Create booking
        booking = BusBooking.objects.create(
            user=request.user,
            bus=bus,
            travel_date=bus.travel_date,
            seat_number=selected_seat,
            price=bus.price,
            booking_status='Pending',
            payment_status='Pending',
            passenger_name='',
            passenger_age=0,
            passenger_gender='Male',
            passenger_phone=''
        )
        return redirect('customer_details', pk=booking.pk)
    context = {
        'bus': bus,
        'booked_seats': booked_seats,
    }
    if bus.bus_seating_type == 'SLEEPER':
        context.update({
            'seats_layout_upper': seats_layout_upper,
            'seats_layout_lower': seats_layout_lower,
        })
    else:
        context.update({
            'seats_layout': seats_layout
        })
    return render(request, 'bus_seats.html', context)
    
    
@login_required(login_url='login')
def customer_details(request, pk):
    booking = get_object_or_404(BusBooking, pk=pk, user=request.user)

    if request.method == "POST":
        form = PassengerForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()

            # booking.booking_status = 'CONFIRMED'
            booking.save()

            bus = booking.bus
            bus.available_seats -= 1
            bus.save()

            messages.success(request, "Booking confirmed successfully")
            return redirect('my_bus_booking')
    else:
        form = PassengerForm(instance=booking)

    return render(request, 'customer_details.html', {
        'form': form,
        'booking': booking
    })
    
def popular_buses(request,pk):
    bus_list =[]
    selected_bus = get_object_or_404(BusModel,pk=pk)
    popular_buses = BusModel.objects.filter(source=selected_bus.source,destination=selected_bus.destination)
    
    for bus in popular_buses:
        dep = bus.departure_time
        arr = bus.arrival_time
        if arr < dep: 
            arr += timedelta(days=1)

        duration = arr - dep
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60

        bus_list.append({
            'bus': bus,
            'duration': f"{hours}h {minutes}m"
        })
        
    paginator = Paginator(bus_list, 5) # Show 5 buses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'all_bus.html', context)

# def generate_seats(total_seats=50):
#     seats = []
#     seat_no = 1

#     while seat_no <= total_seats:
#         row = []

#         # Left side (2 seats)
#         for _ in range(2):
#             if seat_no <= total_seats:
#                 row.append(f"S{seat_no}")
#                 seat_no += 1

#         # Right side (3 seats)
#         for _ in range(3):
#             if seat_no <= total_seats:
#                 row.append(f"S{seat_no}")
#                 seat_no += 1

#         seats.append(row)

#     return seats



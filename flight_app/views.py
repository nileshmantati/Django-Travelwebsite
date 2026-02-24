from django.shortcuts import render,redirect,get_object_or_404
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib import messages
from .models import FlightModel, FlightClass, FlightBooking
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
def flight_search(request):
    flight_list = []
    from_city = request.GET.get('from', '').strip()
    to_city = request.GET.get('to', '').strip()
    price = request.GET.get('price')
    rating = request.GET.get('rating')
    seat_type = request.GET.get('seat_type')
    
    if request.GET.get('today'):
        travel_date = now().date()
    elif request.GET.get('tomorrow'):
        travel_date = now().date() + timedelta(days=1)
    else:
        date_str = request.GET.get('date')
        try:
            travel_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else now().date()
        except (ValueError, TypeError):
            travel_date = now().date()
            
    if from_city and to_city:
        if from_city.lower() == to_city.lower():
            messages.error(request, "From and To cities cannot be the same")
            return redirect('home')
        
        history = request.session.get('search_history', [])
        
        new_search = {
            'from': from_city,
            'to': to_city,
            'date': str(travel_date or now().date()),
            'search_type' : "flight",
            'searched_at': now().isoformat()
        }
        history = [h for h in history if h != new_search]
        history.insert(0, new_search)
        request.session['search_history'] = history[:5]
        
        flights = FlightModel.objects.filter(
            source__name__icontains=from_city,
            destination__name__icontains=to_city,
            travel_date=travel_date,
            is_active=True
        ).prefetch_related('classes')
        
        if travel_date:
            flights = flights.filter(travel_date=travel_date)
            
        if price:
            if price == '0-500':
                flights = flights.filter(price__lt=500)
            elif price == '500-1000':
                flights = flights.filter(price__gte=500, price__lte=1000)
            elif price == '1000+':
                flights = flights.filter(price__gt=1000)

        if rating:
            flights = flights.filter(rating__gte=rating)

        if seat_type:
            flights = flights.filter(bus_seating_type=seat_type)
            
        for flight in flights:
            duration = flight.arrival_time - flight.departure_time
            
            total_seconds = int(duration.total_seconds())
            if total_seconds < 0:
                total_seconds += 86400
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            flight_list.append({
                'bus': None,
                'flight': flight,
                'duration': f"{hours}h {minutes}m"
            })
        paginator = Paginator(flight_list, 4) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'from_city': from_city,
            'to_city': to_city,
            'travel_date': travel_date or now().date(),
            'page_obj': page_obj,
        }
        return render(request, 'flights/search_flight.html',context)
    
    messages.error(request, "Please enter both From and To cities")
    return redirect('home')

@login_required
def load_flight_classes(request, flight_id):
    try:
        flight = get_object_or_404(FlightModel.objects.prefetch_related('classes'), id=flight_id)
        return render(request, 'flights/flight_coach_modal.html', {'flight': flight})
    except Exception as e:
        print(f"Error: {e}")
        from django.http import HttpResponse
        return HttpResponse(f"Internal Server Error: {e}", status=500)

@login_required
def book_flight(request):
    if request.method == "POST":
        flight_id = request.POST.get('flight_id')
        class_id = request.POST.get('class_id')
        
        flight = get_object_or_404(FlightModel, id=flight_id)
        # flight_class = get_object_or_404(FlightClass, id=class_id)
        try:
            with transaction.atomic():
                flight_class = FlightClass.objects.select_for_update().get(id=class_id)
                
                if flight_class.available_seats <= 0:
                    messages.error(request, f"Sorry, no seats available in {flight_class.class_type}")
                    return redirect('home')
                
                seat_no = (flight_class.total_seats - flight_class.available_seats) + 1
                assigned_seat = f"{flight_class.class_type}-{seat_no}"
                
                booking = FlightBooking.objects.create(
                        user=request.user,
                        flight=flight,
                        flight_class=flight_class,
                        passenger_name=request.POST.get('passenger_name'),
                        passenger_age=request.POST.get('passenger_age'),
                        passport_number=request.POST.get('passport_number'),
                        passenger_gender=request.POST.get('passenger_gender'),
                        booking_status='PENDING',
                        seat_number=assigned_seat,
                        price_at_booking=flight_class.base_price
                )
                flight_class.available_seats -= 1
                flight_class.save()
                messages.success(request, f"Booking successful! Your seat is {assigned_seat}")
                return redirect('my_bookings')
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')

def flight_ticket_detail(request, booking_id):
    booking = get_object_or_404(FlightBooking, booking_id=booking_id)
    return render(request, 'flights/ticket_confirmation.html', {'booking': booking})
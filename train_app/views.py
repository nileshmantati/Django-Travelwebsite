from django.shortcuts import render,redirect,get_object_or_404
from train_app.models import TrainBooking, TrainCoach
from train_app.models import TrainModel
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def train_search(request):
    train_list = []
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
        # travel_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
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
            'search_type' : "train",
            'searched_at': now().isoformat()
        }
        history = [h for h in history if h != new_search]
        history.insert(0, new_search)
        request.session['search_history'] = history[:5]
        
        trains = TrainModel.objects.filter(
            source__name__icontains=from_city,
            destination__name__icontains=to_city,
            travel_date=travel_date,
            is_active=True
        ).prefetch_related('coaches')
        
        if travel_date:
            trains = trains.filter(travel_date=travel_date)
            
        if price:
            if price == '0-500':
                trains = trains.filter(price__lt=500)
            elif price == '500-1000':
                trains = trains.filter(price__gte=500, price__lte=1000)
            elif price == '1000+':
                trains = trains.filter(price__gt=1000)

        if rating:
            trains = trains.filter(rating__gte=rating)

        if seat_type:
            trains = trains.filter(bus_seating_type=seat_type)
            
        for train in trains:
            duration = train.arrival_time - train.departure_time
            
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            train_list.append({
                'bus': None,
                'train': train,
                'duration': f"{hours}h {minutes}m"
            })
        paginator = Paginator(train_list, 4) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'from_city': from_city,
            'to_city': to_city,
            'travel_date': travel_date or now().date(),
            'page_obj': page_obj,
        }
        return render(request, 'trains/search_train.html',context)
    
    messages.error(request, "Please enter both From and To cities")
    return redirect('home')

def load_train_coaches(request, train_id):
    train = get_object_or_404(TrainModel, id=train_id)
    coaches = train.coaches.all()
    print(f"Loading coaches for train: {train.train_name}, Coaches found: {coaches.count()}")
    return render(request, 'trains/train_coach_modal.html', {
        'train': train,
        'coaches': coaches
    })
    
@login_required
def book_train(request):
    if request.method == 'POST':
        coach_id = request.POST.get('coach_id')
        passenger_name = request.POST.get('passenger_name')
        passenger_age = request.POST.get('passenger_age')
        passenger_gender = request.POST.get('passenger_gender')
        
        coach = get_object_or_404(TrainCoach, id=coach_id)
        
        try:
            # Model ke .save() method mein pehle se seat-minus logic hai
            booking = TrainBooking.objects.create(
                user=request.user,
                train=coach.train,
                coach=coach,
                passenger_name=passenger_name,
                passenger_age=passenger_age,
                passenger_gender=passenger_gender,
                seat_number=f"{coach.coach_type}-{coach.available_seats}"
            )
            return redirect('ticket_detail', pnr=booking.pnr_number)
            
        except ValueError as e:
            return render(request, 'error.html', {'message': str(e)})

    return redirect('home')

def ticket_detail(request, pnr):
    booking = get_object_or_404(TrainBooking, pnr_number=pnr)
    return render(request, 'trains/ticket_confirmation.html', {'booking': booking})
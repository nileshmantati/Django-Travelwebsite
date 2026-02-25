from django.shortcuts import render,redirect,get_object_or_404
from bus_app.models import BusModel, BusBooking
from train_app.models import TrainBooking
from flight_app.models import FlightBooking
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .forms import LoginForm
from django.utils import timezone
from bus_app.views import bus_search
from train_app.views import train_search
from flight_app.views import flight_search
from django.http import JsonResponse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def universal_search(request):
    search_type = request.GET.get('type')
    
    if search_type == 'bus':
        return bus_search(request)
    elif search_type == 'train':
        return train_search(request)
    elif search_type == 'flight':
        return flight_search(request)
    else:
        messages.error(request, "Invalid search type")
        return redirect('home')
    
def home(request):
    history = request.session.get('search_history', [])
    buses = BusModel.objects.select_related("source", "destination")[:6]
    today = timezone.localdate()
    BusModel.objects.filter(travel_date__lt=today, is_active=True).update(is_active=False)
    context = {
        'buses': buses,
        'history':history
    }
    return render(request,'home.html',context)

def clear_search_history(request):
    if 'search_history' in request.session:
        del request.session['search_history']
    return redirect('home')

def registration_view(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else :
            messages.error(request, "Please correct the errors below")
    else:       
        form = SignupForm()
   
    return render(request,'registrationpage.html',{'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            next_url = request.POST.get('next') or 'home'
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'loginpage.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect('login')

def coming_soon(request, service_name):
    return render(request, 'components/coming_soon.html', {'service_name': service_name.capitalize()})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()
            
            # User Data
            user_email = contact_instance.email
            user_name = contact_instance.name
            user_subject = contact_instance.subject
            from_email = settings.EMAIL_HOST_USER

            try:
                # Admin Data for sending email to admin
                admin_subject = f"New Inquiry: {user_subject}"
                admin_content = f"Name: {user_name}\nEmail: {user_email}\nSubject: {user_subject}\nMessage: {contact_instance.message}"
                
                send_mail(
                    admin_subject,
                    admin_content,
                    from_email,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                # User Data for sending email to user
                html_subject = 'We have received your inquiry - TravelGo'
                html_message = render_to_string('emails/thank_you.html', {
                    'name': user_name,
                    'subject': user_subject
                })
                plain_message = strip_tags(html_message)

                msg = EmailMultiAlternatives(html_subject, plain_message, from_email, [user_email])
                msg.attach_alternative(html_message, "text/html")
                msg.send()

                messages.success(request, "Thank you! Your inquiry has been successfully submitted.")
                
            except Exception as e:
                messages.warning(request, "Your inquiry was saved, but we encountered a technical issue while sending the confirmation email.")
                print(f"Email Error: {e}")

            return redirect('contact')
    else:
        form = ContactForm()
        
    return render(request, 'contactpage.html', {'form': form})

@login_required(login_url='login')
def my_bookings(request):
    bus_bookings = BusBooking.objects.filter(user=request.user).order_by('-booked_at')
    train_bookings = TrainBooking.objects.filter(user=request.user).order_by('-booked_at')
    flight_bookings = FlightBooking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'my_bookings.html', {
        'bus_bookings': bus_bookings,
        'train_bookings': train_bookings,
        'flight_bookings': flight_bookings
    })

@login_required(login_url='login')
def cancel_booking(request, booking_type, pk):
    if booking_type == 'bus':
        model = BusBooking
    elif booking_type == 'train':
        model = TrainBooking
    elif booking_type == 'flight':
        model = FlightBooking
    else:
        messages.error(request, "Invalid booking type!")
        return redirect('home')
    
    booking = get_object_or_404(model, pk=pk, user=request.user)
    try:
        booking.cancel()
        return JsonResponse({
            'status': 'success', 
            'message': f'{booking_type.capitalize()} booking cancelled successfully!'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
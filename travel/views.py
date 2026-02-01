from django.shortcuts import render,redirect
from bus_app.models import BusModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from .forms import LoginForm
from django.utils import timezone

# Create your views here.
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

from django.shortcuts import render,get_object_or_404,redirect
from bus_app.models import BusModel, BusBooking, City
from train_app.models import TrainModel, TrainBooking
from django.contrib.auth.models import User
from user_dashboard.forms import UserProfileForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def staff_required(user):
    if user.is_authenticated and user.is_staff:
        return True
    raise PermissionDenied


def superuser_required(user):
    if user.is_authenticated and user.is_superuser:
        return True
    raise PermissionDenied


@login_required
def user_dashboard(request):
    user = request.user
    confirmed_bus = BusBooking.objects.filter(user=user, booking_status='CONFIRMED').count()
    all_bus_trips = BusBooking.objects.filter(user=user).count()
    confirmed_train = TrainBooking.objects.filter(user=user, booking_status='CONFIRMED').count()
    context = {
        'total_trips': confirmed_bus + confirmed_train, # Combined confirmed trips
        'My_bus_trips': all_bus_trips,
        'My_train_trips': confirmed_train,
    }
    return render(request, 'user_dashboard/user_dashboard.html',context)

@login_required
def user_profile(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    
    if request.method == 'POST':
        if 'profile_img' in request.FILES:
            if profile:
                profile.profile_img = request.FILES['profile_img']
                profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
        
    profile_form = ProfileForm(instance=profile)
    context={
        'user':user,
        'profile_form':profile_form,
    }
    return render(request,'user_dashboard/profile.html',context)

@login_required
def edit_profile(request,pk):
    user = request.user
    if user.id != pk:
        raise PermissionDenied

    user = get_object_or_404(User, pk=pk)
    profile = getattr(user, 'profile', None)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user  
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
            print("Form Errors:", user_form.errors)
            print("Form Errors:", profile_form.errors)
            
    user_form = UserProfileForm(instance=user)
    profile_form = ProfileForm(instance=profile)
    return render(request,'user_dashboard/edit_profile.html',{'user_form':user_form,'profile_form':profile_form,'title':'Edit Profile'})
        

@login_required
def user_bus_bookings(request):    
    user = request.user
    userid = user.id
    bookings = BusBooking.objects.filter(user_id=userid).order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'user_dashboard/user_bus_bookings.html',context)     

@login_required
def user_train_bookings(request):
    user = request.user
    userid = user.id
    bookings = TrainBooking.objects.filter(user_id=userid).order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'user_dashboard/user_train_bookings.html',context)  
from django.shortcuts import render,get_object_or_404,redirect
from bus_app.models import BusModel, BusBooking, City
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
    userid = user.id
    user_trips = BusBooking.objects.filter(user_id=userid,booking_status='CONFIRMED')
    user_bookings = BusBooking.objects.filter(user_id=userid)
    # user_active_bookings = BusBooking.objects.filter(user_id=userid,bus__is_active=True)
    total_users = request.user.__class__.objects.all()
    context = {
        'total_trips':user_trips.count() ,
        # 'active_bookings' :user_active_bookings.count() ,
        'My_bookings' :user_bookings.count() ,
        'total_users' :total_users.count() ,
    }
    return render(request, 'user_dashboard/user_dashboard.html',context)

@login_required
def user_bookings(request):
    user = request.user
    userid = user.id
    bookings = BusBooking.objects.filter(user_id=userid).order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'dashboard/bookings.html',context)

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
        
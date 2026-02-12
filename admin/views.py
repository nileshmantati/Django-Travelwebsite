from django.shortcuts import render ,redirect,get_object_or_404
from bus_app.models import BusModel,BusBooking,City
from train_app.models import TrainModel,TrainCoach,TrainBooking
from admin.forms import BusForm , UserForm, CityForm, TrainForm, TrainCoachForm
from django.forms import inlineformset_factory
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    total_buses = BusModel.objects.all()
    total_trains = TrainModel.objects.all()
    total_cities = City.objects.all()
    total_bus_bookings = BusBooking.objects.all()
    total_train_bookings = TrainBooking.objects.all()
    total_users = request.user.__class__.objects.all()
    context = {
        'total_buses':total_buses.count() ,
        'total_trains':total_trains.count() ,
        'total_cities' :total_cities.count() ,
        'total_bus_bookings' :total_bus_bookings.count() ,
        'total_train_bookings' :total_train_bookings.count() ,
        'total_users' :total_users.count() ,
    }
    return render(request,'dashboard/dashboard.html',context)

# City Views
@login_required
def city_list(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    cities = City.objects.all()
    return render(request,'dashboard/city_list.html',{'cities':cities})

@login_required
def add_city(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "City added successfully!")
            return redirect('city_list')
        else:
            messages.error(request, "City name cannot be empty.")
            return redirect('add_city')
    else:
        form = CityForm()
    return render(request,'dashboard/add_city.html',{'form':form,'title':'Add New City'})


@login_required
def edit_city(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST,request.FILES,instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, "City updated successfully!")
            return redirect('city_list')
        else:
            messages.error(request, "City name cannot be empty.")
            return redirect('edit_city')
    else:
        form = CityForm(instance=city)
        
    return render(request,'dashboard/edit_city.html',{'form':form,'title':'Edit City'})

@login_required
def delete_city(request,pk):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        city = get_object_or_404(City, pk=pk)
        cityname = city.name
        city.delete()
        messages.success(request, f"City '{cityname}' has been deleted successfully!")
    return redirect('city_list')

# buses Views
@login_required
def bus_list(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    buses = BusModel.objects.all()
    return render(request,'dashboard/bus_list.html',{'buses':buses})

@login_required
def add_bus(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = BusForm(request.POST, request.FILES) # Files image ke liye zaroori hai
        if form.is_valid():
            form.save()
            messages.success(request, "Bus added successfully!")
            return redirect('bus_list')
        else:
            messages.error(request, "Please correct the errors below.")
            print("Form Errors:", form.errors)
    else:
        form = BusForm()
    return render(request,'dashboard/add_bus.html',{'form':form,'title':'Add New Bus'})

@login_required
def edit_bus(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied

    bus = get_object_or_404(BusModel, pk=pk)
    if request.method == "POST":
        form = BusForm(request.POST, request.FILES, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus updated successfully!")
            return redirect('bus_list')
        else:
            messages.error(request, "Please correct the errors below.")
            print("Form Errors:", form.errors)
    form = BusForm(instance=bus)
    return render(request, 'dashboard/edit_bus.html', {'form': form, 'title': 'Edit Bus'})

@login_required
def change_bus_status(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    bus = get_object_or_404(BusModel, pk=pk)
    bus.is_active = not bus.is_active
    bus.save()
    status_str = "Activated" if bus.is_active else "Deactivated"
    messages.info(request, f"Bus '{bus.bus_name}' has been {status_str}.")
    return redirect('bus_list')

@login_required
def delete_bus(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        bus = get_object_or_404(BusModel, pk=pk)
        bus_name = bus.bus_name
        bus.delete()
        messages.success(request, f"Bus '{bus_name}' has been deleted successfully!")
    return redirect('bus_list')

# Users Views
@login_required
def users(request):
    if not request.user.is_staff:
        raise PermissionDenied
    users = User.objects.all()
    context={
        'users':users
    }
    return render(request,'dashboard/users.html',context)

@login_required
def add_user(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect('users')
    else:
        form = UserForm()
    return render(request,'dashboard/add_user.html',{
        'form': form, 
        'title': 'Add New User'
    })
    
@login_required
def edit_user(request,pk):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('users')
        else:
            messages.error(request, "Please correct the errors below.")
            print("Form Errors:", form.errors)
    form = UserForm(instance=user)
    return render(request, 'dashboard/edit_user.html', {'form': form, 'title': 'Edit User'})

@login_required
def delete_user(request,pk):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' has been deleted successfully!")
    return redirect('users')
    
# Train Views
@login_required
def train_list(request):
    if not request.user.is_staff:
        raise PermissionDenied
    trains = TrainModel.objects.prefetch_related('coaches').all()
    context={
        'trains':trains
    }
    return render(request,'dashboard/train_list.html',context)

@login_required
def add_train(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    CoachFormSet = inlineformset_factory(
        TrainModel, 
        TrainCoach, 
        fields=['coach_type', 'total_seats', 'available_seats', 'price'],
        extra=1, 
        can_delete=True,
        widgets={
            'coach_type': forms.Select(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    )
    
    if request.method == 'POST':
        form = TrainForm(request.POST)
        formset = CoachFormSet(request.POST, prefix='coaches')

        if form.is_valid() and formset.is_valid():
            train_instance = form.save()
            formset.instance = train_instance
            formset.save()
            return redirect('train_list')
    else:
        form = TrainForm()
        formset = CoachFormSet(prefix='coaches')

    return render(request, 'dashboard/add_train.html', {
        'form': form,
        'formset': formset
    })
    
@login_required
def edit_train(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    train = get_object_or_404(TrainModel, pk=pk)
    CoachFormSet = inlineformset_factory(
        TrainModel, 
        TrainCoach, 
        fields=['coach_type', 'total_seats', 'available_seats', 'price'],
        extra=1, 
        can_delete=True,
        widgets={
            'coach_type': forms.Select(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    )
    
    if request.method == 'POST':
        form = TrainForm(request.POST,instance=train)
        formset = CoachFormSet(request.POST,instance=train,prefix='coaches')

        if form.is_valid() and formset.is_valid():
            train_instance = form.save()
            formset.instance = train_instance
            formset.save()
            return redirect('train_list')
    else:
        form = TrainForm(instance=train)
        formset = CoachFormSet(instance=train,prefix='coaches')
    
    return render(request,'dashboard/edit_train.html',{'form': form, 'formset': formset})

@login_required
def change_train_status(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    train = get_object_or_404(TrainModel, pk=pk)
    train.is_active = not train.is_active
    train.save()
    status_str = "Activated" if train.is_active else "Deactivated"
    trainname =train.train_name
    messages.info(request, f"Train '{trainname}' has been {status_str}.")
    return redirect('train_list')

@login_required
def delete_train(request,pk):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        train = get_object_or_404(TrainModel, pk=pk)
        trainname = train.train_name
        train.delete() 
        messages.success(request, f"Train '{trainname}' has been deleted successfully!") 
    return redirect('train_list')
        
   
# Booking Views
@login_required
def bus_bookings(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    bookings = BusBooking.objects.all().order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'dashboard/bus_bookings.html',context)     

@login_required
def train_bookings(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    bookings = TrainBooking.objects.all().order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'dashboard/train_bookings.html',context)  
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES) # Files image ke liye zaroori hai
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Product added successfully!")
#             return redirect('product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'dashboard/products/product_form.html', {'form': form, 'title': 'Add New Product'})
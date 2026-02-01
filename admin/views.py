from django.shortcuts import render ,redirect,get_object_or_404
from bus_app.models import BusModel,BusBooking,City
from admin.forms import BusForm , UserForm
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


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    total_buses = BusModel.objects.all()
    total_cities = City.objects.all()
    total_bookings = BusBooking.objects.all()
    total_users = request.user.__class__.objects.all()
    context = {
        'total_buses':total_buses.count() ,
        'total_cities' :total_cities.count() ,
        'total_bookings' :total_bookings.count() ,
        'total_users' :total_users.count() ,
    }
    return render(request,'dashboard/dashboard.html',context)

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

@login_required
def bookings(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    bookings = BusBooking.objects.all().order_by('-booked_at')
    context={
        'bookings':bookings
    }
    return render(request,'dashboard/bookings.html',context)

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
from django import forms
from bus_app.models import BusModel
from django.contrib.auth.models import User

class BusForm(forms.ModelForm):
    class Meta:
        model = BusModel
        fields = '__all__'

        widgets = {
            'bus_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MH-12-AB-1234'}),
            'bus_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bus name'}),
            'bus_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'AC / Non-AC'}),
            'bus_seating_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sleeper / Seater'}),
            
            # Use NumberInput for numeric data to trigger number pad on mobile
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'max': '5', 'min': '0'}),

            'source': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Starting City'}),
            'destination': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ending City'}),

            # Use Date/Time inputs for native mobile pickers
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),

            # Boolean fields are usually better as Checkboxes or Selects
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # Yeh line password ko hash (encrypt) karne ke liye zaroori hai
        # user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
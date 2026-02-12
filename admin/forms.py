from django import forms
from bus_app.models import BusModel,City
from train_app.models import TrainModel, TrainCoach
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
        
DAYS_CHOICES = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
]
        
class TrainForm(forms.ModelForm):
    runs_on = forms.MultipleChoiceField(
        choices=DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled d-flex flex-wrap gap-3'
        }),
        help_text="Select days when this train operates"
    )
    class Meta:
        model = TrainModel
        fields = ['train_number', 'train_name', 'source', 'destination', 
                  'departure_time', 'arrival_time', 'travel_date', 'runs_on', 'is_active']
        exclude = ['runs_on']
        
        widgets = {
            'train_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12121'}),
            'train_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Train Name'}),
            
            'source': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),

            # Date aur Time ke liye native pickers
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),

            # 'runs_on': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mon, Wed, Fri'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }
        
        def clean_runs_on(self):
            data = self.cleaned_data.get('runs_on')
            return ", ".join(data) if data else ""
        
class TrainCoachForm(forms.ModelForm):
    class Meta:
        model = TrainCoach
        fields = ['coach_type', 'total_seats', 'available_seats', 'price']
        
        widgets = {
            'coach_type': forms.Select(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
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
    
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.title() if name else name
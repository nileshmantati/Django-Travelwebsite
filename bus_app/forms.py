from django import forms
from .models import BusBooking

class PassengerForm(forms.ModelForm):
    class Meta:
        model = BusBooking
        fields = [
            'passenger_name',
            'passenger_age',
            'passenger_gender',
            'passenger_phone'
        ]
        widgets = {
            'passenger_name': forms.TextInput(attrs={'class': 'form-control'}),
            'passenger_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'passenger_gender': forms.Select(attrs={'class': 'form-control'}),
            'passenger_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

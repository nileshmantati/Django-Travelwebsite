from django import forms
from django.contrib.auth.models import User    
from travel.models import Profile 
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # Yeh line password ko hash (encrypt) karne ke liye zaroori hai
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img', 'phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            # 'profile_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_img': forms.FileInput(attrs={'class': 'form-control','onchange': 'previewImage(event)'}),
        }
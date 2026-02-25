from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_img = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(max_length=1000)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
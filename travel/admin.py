from django.contrib import admin
from .models import Profile, Contact

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
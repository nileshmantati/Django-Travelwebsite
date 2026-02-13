from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.user_dashboard, name="user_dashboard"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('user_profile/edit_profile/<int:pk>/', views.edit_profile, name="edit_profile"),    
    path('user_bus_bookings/', views.user_bus_bookings, name="user_bus_bookings"),
    path('user_train_bookings/', views.user_train_bookings, name="user_train_bookings"),
]
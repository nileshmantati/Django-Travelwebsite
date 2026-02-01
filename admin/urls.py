from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('buses/', views.bus_list, name="bus_list"),
    path('add_bus/', views.add_bus, name="add_bus"),
    path('edit_bus/<int:pk>/', views.edit_bus, name="edit_bus"),
    path('delete_bus/<int:pk>/', views.delete_bus, name="delete_bus"),
    path('change_bus_status/<int:pk>/', views.change_bus_status, name='change_bus_status'),
    path('bookings/', views.bookings, name="bookings"),
    path('users/', views.users, name="users"),
    path('users/add_user/', views.add_user, name="add_user"),
    path('users/edit_user/<int:pk>/', views.edit_user, name="edit_user"),
    path('users/delete_user/<int:pk>/', views.delete_user, name="delete_user"),
    
]
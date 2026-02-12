from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name="admin_dashboard"),
    
    # City urls
    path('cities/', views.city_list, name="city_list"),
    path('city/add_city/', views.add_city, name="add_city"),
    path('city/edit_city/<int:pk>/', views.edit_city, name="edit_city"),
    path('city/delete_city/<int:pk>/', views.delete_city, name="delete_city"),
    
    # Bus urls
    path('buses/', views.bus_list, name="bus_list"),
    path('add_bus/', views.add_bus, name="add_bus"),
    path('edit_bus/<int:pk>/', views.edit_bus, name="edit_bus"),
    path('delete_bus/<int:pk>/', views.delete_bus, name="delete_bus"),
    path('change_bus_status/<int:pk>/', views.change_bus_status, name='change_bus_status'),
    
    # Train Urls
    path('trains/',views.train_list,name="train_list"),
    path('train/add_train/',views.add_train,name="add_train"),
    path('train/edit_train/<int:pk>/',views.edit_train,name="edit_train"),
    path('train/change_train_status/<int:pk>/', views.change_train_status, name='change_train_status'),
    path('train/delete_train/<int:pk>/',views.delete_train,name="delete_train"),
    
    # All Bokkings
    path('bus_bookings/', views.bus_bookings, name="bus_bookings"),
    path('train_bookings/', views.train_bookings, name="train_bookings"),
    
    # Users urls
    path('users/', views.users, name="users"),
    path('users/add_user/', views.add_user, name="add_user"),
    path('users/edit_user/<int:pk>/', views.edit_user, name="edit_user"),
    path('users/delete_user/<int:pk>/', views.delete_user, name="delete_user"),
    
]
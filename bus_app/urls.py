from django.urls import path
from . import views

urlpatterns = [
    path('search/',views.bus_search,name='bus_search'),
    path('popular_buses/<int:pk>/',views.popular_buses,name='popular_buses'),
    path('bus/<int:pk>/seats/', views.bus_seat_view, name='bus_seats'),
    path('customer-details/<int:pk>/', views.customer_details, name='customer_details'),
    path('my-bus-booking/', views.my_bus_booking, name='my_bus_booking'),
    path('cancel-booking/<str:pk>/', views.cancel_booking, name='cancel_booking'),
]
    
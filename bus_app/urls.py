from django.urls import path
from . import views

urlpatterns = [
    path('popular_buses/<int:pk>/',views.popular_buses,name='popular_buses'),
    path('bus/<int:pk>/seats/', views.bus_seat_view, name='bus_seats'),
    path('customer-details/<int:pk>/', views.customer_details, name='customer_details'),
]
    
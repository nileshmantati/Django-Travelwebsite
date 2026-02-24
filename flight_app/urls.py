from django.urls import path
from . import views

urlpatterns = [
    path('classes/<int:flight_id>/', views.load_flight_classes, name='load_flight_classes'),
    path('book_flight/', views.book_flight, name='book_flight'),
    path('flight_ticket/<int:id>/', views.flight_ticket_detail, name='flight_ticket_detail'),
]
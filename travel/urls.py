from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.universal_search,name='search'),
    path('clear-history/', views.clear_search_history, name='clear_search_history'),
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('flights/', views.coming_soon, {'service_name': 'flight'}, name='flight_booking'),
    path('trains/', views.coming_soon, {'service_name': 'train'}, name='train_booking'),
    path('hotels/', views.coming_soon, {'service_name': 'hotel'}, name='hotel_booking'),
    path('contact/', views.coming_soon, {'service_name': 'contact'}, name='contact'),
    path('my-bus-booking/', views.my_bus_booking, name='my_bus_booking'),
    path('cancel-booking/<str:pk>/', views.cancel_booking, name='cancel_booking'),
]
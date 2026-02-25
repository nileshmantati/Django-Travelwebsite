from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.universal_search,name='search'),
    path('clear-history/', views.clear_search_history, name='clear_search_history'),
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('contact/', views.contact, name='contact'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<str:booking_type>/<str:pk>/', views.cancel_booking, name='cancel_booking'),
]
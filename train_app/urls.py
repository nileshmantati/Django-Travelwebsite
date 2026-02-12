from django.urls import path
from . import views

urlpatterns = [
    path('coaches/<int:train_id>/', views.load_train_coaches, name='load_train_coaches'),
    path('book/', views.book_train, name='book_train'),
    path('ticket/<str:pnr>/', views.ticket_detail, name='ticket_detail'),
]
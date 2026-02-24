from django.urls import path
from . import views

urlpatterns = [
    path('coaches/<int:train_id>/', views.load_train_coaches, name='load_train_coaches'),
    path('book/', views.book_train, name='book_train'),
    path('train_ticket/<str:pnr>/', views.train_ticket_detail, name='train_ticket_detail'),
]
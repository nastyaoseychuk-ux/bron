from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('hotels/<int:id>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    path('rooms/<int:id>/room/', views.room, name='room'),
    path('rooms/<int:id>/booking/', views.booking, name='booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/<int:id>/delete/', views.delete_booking, name='delete_booking'),
]
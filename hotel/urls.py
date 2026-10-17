from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('hotels/<int:id>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    path('rooms/<int:id>/room/', views.room, name='room'),
]
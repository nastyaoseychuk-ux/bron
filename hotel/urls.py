from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel'),
    path('rooms/<int:id>/', views.room, name='room'),
]
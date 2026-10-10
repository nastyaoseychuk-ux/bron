from django.shortcuts import render
from  hotel.models import Room, Hotel, Booking, RoomImage, Location, HotelImage, Review, Amenite
def hotel(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def room(request, id):
    room = Room.objects.get(id=id)
    return render(request, 'rooms.html', {'room': room})
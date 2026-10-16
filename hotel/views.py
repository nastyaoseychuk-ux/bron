
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room


def hotel(request):
    hotels = Hotel.objects.select_related('location').prefetch_related(
        'images', 'amenities', 'rooms'
    )

    return render(request, 'home.html', {'hotels': hotels})


def hotel_rooms(request, id):
    hotel = get_object_or_404(Hotel, id=id)

    return render(request, 'hotel_rooms.html', {
        'hotel': hotel,
        'rooms': hotel.rooms.all(),
    })


def room(request, id):
    room = get_object_or_404(Room, id=id)

    return render(request, 'rooms.html', {'room': room})

from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Hotel, Room
from .forms import BookingForm

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

    return render(request, 'room.html', {'room': room})

@login_required
def booking(request, id):
    room = get_object_or_404(Room.objects.select_related('hotel__location'), id=id)
    form = BookingForm(
        request.POST or None,
        room=room,
        initial={
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        },
    )

    if request.method == 'POST' and form.is_valid():
        new_booking = form.save(commit=False)
        new_booking.user = request.user
        new_booking.room = room
        new_booking.hotel = room.hotel
        new_booking.save()
        return render(request, 'booking.html', {'room': room, 'booking': new_booking})

    return render(request, 'booking.html', {'room': room, 'form': form})
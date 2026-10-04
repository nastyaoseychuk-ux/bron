from django.contrib import admin
from .models import Hotel, Room, Booking, RoomImage, User, Location, HotelImage, Review, Amenite

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(HotelImage)
admin.site.register(RoomImage)
admin.site.register(Review)
admin.site.register(Amenite)
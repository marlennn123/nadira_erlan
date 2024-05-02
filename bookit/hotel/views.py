from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
class HotelViewSets(viewsets.ModelViewSet):
	queryset = Hotel.objects.all()
	serializer_class = HotelSerializer
class RoomViewSets(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
class PhotoRoomViewSets(viewsets.ModelViewSet):
	queryset = PhotoRoom.objects.all()
	serializer_class = PhotoRoomSerializer
class BookingViewSets(viewsets.ModelViewSet):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
class UserProfileViewSets(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
class CommentViewSets(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
class PhotoViewSets(viewsets.ModelViewSet):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer
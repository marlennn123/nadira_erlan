from requests import Response
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.db.models import Avg


class HotelViewSets(viewsets.ModelViewSet):
    queryset = Hotel.objects.annotate(rating=Avg('comment__rating'))
    serializer_class = HotelSerializer


class HotelDetailViewSets(viewsets.ModelViewSet):
    queryset = Hotel.objects.annotate(rating=Avg('comment__rating'))
    serializer_class = HotelDetailSerializer


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



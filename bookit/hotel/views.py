from rest_framework import viewsets
from .models import *
from .serializers import *
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters


class HotelFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lt')

    class Meta:
        model = Hotel
        fields = ['country', 'city', 'rating']


class HotelViewSets(viewsets.ModelViewSet):
    queryset = Hotel.objects.annotate(rating=Avg('comment__rating'))
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HotelFilter
    ordering_fields = ('rating',)


class HotelDetailViewSets(viewsets.ModelViewSet):
    queryset = Hotel.objects.annotate(rating=Avg('comment__rating'))
    serializer_class = HotelDetailSerializer


class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_number',]


class BookingViewSets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class UserProfileViewSets(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CommentViewSets(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



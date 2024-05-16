from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('hotel/', HotelViewSets.as_view({'get': 'list', 'post': 'create'}),
         name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='hotel_detail'),
    path('room/', RoomViewSets.as_view({'get': 'list', 'post': 'create'}),
         name='room_list'),
    path('room/<int:pk>/', RoomViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='room_detail'),
    path('booking/', BookingViewSets.as_view({'get': 'list', 'post': 'create'}),
         name='booking_list'),
    path('booking/<int:pk>/', BookingViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='booking_detail'),
    path('userprofile/', UserProfileViewSets.as_view({'get': 'list', 'post': 'create'}),
         name='userprofile_list'),
    path('userprofile/<int:pk>/',
         UserProfileViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='userprofile_detail'),
    path('comment/', CommentViewSets.as_view({'get': 'list', 'post': 'create'}),
         name='comment_list'),
    path('comment/<int:pk>/', CommentViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='comment_detail'),
]

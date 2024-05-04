from rest_framework import serializers
from .models import *


class HotelSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_photos(self, obj):
        request = self.context.get('request')
        if request is not None:
            return [request.build_absolute_uri(photo.image.url) for photo in obj.photos.all()] if obj.photos.exists() else []
        else:
            return []

    def get_rating(self, obj):
        return round(obj.rating) if obj.rating is not None else 0

    def get_characteristics(self, obj):
        characteristics = obj.characteristics.all()
        characteristics_dict = {}
        for characteristic in characteristics:
            characteristics_dict[characteristic.key] = characteristic.value
        return characteristics_dict


class CommentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    hotel = serializers.SlugRelatedField(slug_field="name", queryset=Hotel.objects.all())
    user = serializers.SlugRelatedField(slug_field="first_name", queryset=UserProfile.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class HotelDetailSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(default=0, read_only=True)
    photos = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_photos(self, obj):
        request = self.context.get('request')
        if request is not None:
            return [request.build_absolute_uri(photo.image.url) for photo in obj.photos.all()] if obj.photos.exists() \
                else []
        else:
            return []

    def get_characteristics(self, obj):
        characteristics = obj.characteristics.all()
        characteristics_dict = {}
        for characteristic in characteristics:
            characteristics_dict[characteristic.key] = characteristic.value
        return characteristics_dict

    def get_comment(self, obj):
        comment = Comment.objects.filter(hotel=obj)
        return self.get_recursive_comments(comment)

    def get_recursive_comments(self, comments):
        serialized_comments = []
        for comment in comments:
            serialized_comment = CommentSerializer(comment).data
            if comment.parent:
                serialized_comment['parent'] = self.get_recursive_comments([comment.parent])[0]
            else:
                serialized_comment.pop('parent')  # Удаляем поле parent, если оно равно None
            serialized_comments.append(serialized_comment)
        return serialized_comments


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.SlugRelatedField(slug_field="name", queryset=Hotel.objects.all())
    photos = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_photos(self, obj):
        request = self.context.get('request')
        if request is not None:
            return [request.build_absolute_uri(photo.image.url) for photo in obj.photos.all()] if obj.photos.exists() else []
        else:
            return []

    def get_user(self, obj):  # Add this method
        bookings = obj.bookings.all()
        if bookings.exists():
            return ', '.join([str(booking.user) for booking in bookings])
        else:
            return "No bookings for this room"


class PhotoRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoRoom
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="first_name", queryset=UserProfile.objects.all())
    # room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())  # Используем PrimaryKeyRelatedField для комнаты
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price']

    def get_total_price(self, obj):
        total_price = (obj.check_out_date - obj.check_in_date).days * obj.room.price_per_night
        return total_price

    def validate(self, data):
        room = data.get('room')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')

        # Проверяем, не забронирована ли комната на указанные даты
        existing_bookings = Booking.objects.filter(room=room, status='Активно')
        conflicting_bookings = existing_bookings.filter(
            check_in_date__lte=check_out_date,
            check_out_date__gte=check_in_date
        )
        if self.instance:
            conflicting_bookings = conflicting_bookings.exclude(pk=self.instance.pk)
        if conflicting_bookings.exists():
            raise serializers.ValidationError('Эта комната уже забронирована на указанные даты.')

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'






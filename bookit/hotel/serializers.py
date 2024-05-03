from rest_framework import serializers
from .models import *
from django.urls import reverse


class HotelSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(default=0, read_only=True)
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
            return [request.build_absolute_uri(photo.image.url) for photo in obj.photos.all()] if obj.photos.exists() else []
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
    class Meta:
        model = Room
        fields = '__all__'


class PhotoRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoRoom
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'






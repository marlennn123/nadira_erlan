from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    country = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='images/user/', blank=True, null=True)
    phone_number = models.DecimalField(max_digits=12, decimal_places=0)
    email = models.EmailField()

    def __str__(self):
        return self.user


class Photo(models.Model):
    image = models.ImageField(upload_to='images/hotel')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='characteristics')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f' {self.key} - {self.value}'


class Hotel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=20, unique=True)
    rating = models.IntegerField(default=0)
    photos = models.ManyToManyField(Photo, blank=True, related_name='photos')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                 help_text="Rate the item with 0 to 6 stars.",
                                 verbose_name="Rating")

    def __str__(self):
        return f'{self.user} - {self.hotel.name}'


class PhotoRoom(models.Model):
    image = models.ImageField(upload_to='images/room/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CharacteristicRoom(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='characteristics_room')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f' {self.key} - {self.value}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.IntegerField(default=1)
    capacity = models.IntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    photos = models.ManyToManyField(PhotoRoom, blank=True, related_name='photos')

    def __str__(self):
        return f'{self.hotel} - {self.room_number}'


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField(auto_now=True)
    check_out_date = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Активно', 'Активно'),
        ('Бронь', 'Бронь'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Активно')

    def save(self, *args, **kwargs):
        if not self.id:
            self.total_price = self.room.price_per_night * (self.check_out_date - self.check_in_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.room} - {self.total_price}'


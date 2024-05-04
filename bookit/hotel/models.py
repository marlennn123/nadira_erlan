from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    country = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='images/user/', blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Photo(models.Model):
    image = models.ImageField(upload_to='images/hotel')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    """
    Характеристика для отеля или комнаты
    """

    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='characteristics', null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='characteristics', null=True, blank=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)


class Hotel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    photos = models.ManyToManyField(Photo, blank=True, related_name='photos')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotels', default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    STATUS_CHOICES = (
        ('Активно', 'Активно'),
        ('Бронь', 'Бронь'),
        ('Завершено', 'Завершено'),
        ('Отменено', 'Отменено'),
        ('В ожидании', 'В ожидании'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Активно')

    def __str__(self):
        return f'{self.user} - {self.room}'

    def clean(self):
        # Проверяем, не забронирована ли комната на указанные даты
        existing_bookings = Booking.objects.filter(room=self.room, status='Активно')
        conflicting_bookings = existing_bookings.filter(
            check_in_date__lte=self.check_out_date,  # Включаем совпадающие даты
            check_out_date__gte=self.check_in_date
        )
        if self.pk:  # Проверяем, это обновление существующего бронирования или новое
            conflicting_bookings = conflicting_bookings.exclude(pk=self.pk)
        if conflicting_bookings.exists():
            raise ValidationError('Эта комната уже забронирована на указанные даты.')
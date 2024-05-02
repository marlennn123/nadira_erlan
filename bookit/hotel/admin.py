from django.contrib import admin
from .models import *


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


class CharacteristicRoomInline(admin.TabularInline):
    model = CharacteristicRoom
    extra = 1


class HotelAdmin(admin.ModelAdmin):
    inlines = [CharacteristicInline]

    def display_characteristics(self, obj):
        return ', '.join([f'{item.key}: {item.value}' for item in obj.characteristics.all()])

    display_characteristics.short_description = 'Characteristics'


class RoomAdmin(admin.ModelAdmin):
    inlines = [CharacteristicRoomInline]

    def display_characteristics(self, obj):
        return ', '.join([f'{item.key}: {item.value}' for item in obj.characteristics.all()])

    display_characteristics.short_description = 'Characteristics_room'


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(PhotoRoom)
admin.site.register(Photo)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Comment)


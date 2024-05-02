from django.contrib import admin
from .models import *


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


class Admin(admin.ModelAdmin):
    inlines = [CharacteristicInline]

    def display_characteristics(self, obj):
        return ', '.join([f'{item.key}: {item.value}' for item in obj.characteristics.all()])

    display_characteristics.short_description = 'Characteristics'


admin.site.register(Hotel, Admin)
admin.site.register(Room, Admin)
admin.site.register(PhotoRoom)
admin.site.register(Photo)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Comment)


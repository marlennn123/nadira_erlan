# Generated by Django 5.0.4 on 2024-05-03 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_remove_room_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='hotel.hotel'),
        ),
    ]

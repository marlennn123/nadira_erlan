# Generated by Django 5.0.4 on 2024-05-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_alter_booking_check_in_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Активно', 'Активно'), ('Бронь', 'Бронь'), ('Завершено', 'Завершено'), ('Отменено', 'Отменено'), ('В ожидании', 'В ожидании')], default='Активно', max_length=20),
        ),
    ]

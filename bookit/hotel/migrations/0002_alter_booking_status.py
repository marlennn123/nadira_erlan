# Generated by Django 5.0.4 on 2024-05-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Активно', 'Активно'), ('Бронь', 'Бронь'), ('Завершено', 'Завершено'), ('Отменено', 'Отменено'), ('В ожидании', 'В ожидании')], default='Бронь', max_length=20),
        ),
    ]
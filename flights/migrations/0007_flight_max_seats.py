# Generated by Django 5.0.3 on 2024-03-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_reservation_seat_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='max_seats',
            field=models.PositiveIntegerField(default=125),
        ),
    ]

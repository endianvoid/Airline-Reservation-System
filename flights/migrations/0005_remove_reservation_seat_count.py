# Generated by Django 5.0.3 on 2024-03-30 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_remove_reservation_seat_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='seat_count',
        ),
    ]
# Generated by Django 5.0.3 on 2024-03-30 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_alter_flight_arrival_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='family_members',
        ),
    ]

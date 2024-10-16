# Generated by Django 4.2.14 on 2024-10-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0025_remove_hotelimages_hotel_request_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='cancelable_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookings',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
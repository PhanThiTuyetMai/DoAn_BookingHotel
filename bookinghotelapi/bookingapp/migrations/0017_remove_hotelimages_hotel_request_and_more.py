# Generated by Django 4.2.14 on 2024-09-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0016_remove_hotelimages_hotel_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='adults',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='children',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='pets',
            field=models.IntegerField(default=0),
        ),
    ]

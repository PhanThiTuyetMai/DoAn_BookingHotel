# Generated by Django 4.2.14 on 2024-09-17 09:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0007_remove_hotelimages_hotel_request_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelrequest',
            name='active',
        ),
        migrations.AlterField(
            model_name='hotelrequest',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

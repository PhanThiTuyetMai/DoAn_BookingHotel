# Generated by Django 4.2.14 on 2024-09-17 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimages',
            name='hotel_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bookingapp.hotelrequest'),
        ),
    ]

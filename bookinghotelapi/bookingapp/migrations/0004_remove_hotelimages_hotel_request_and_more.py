# Generated by Django 4.2.14 on 2024-09-17 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingapp', '0003_hotelimages_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelimages',
            name='hotelrequest',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookingapp.hotelrequest'),
        ),
    ]

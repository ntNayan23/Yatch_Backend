# Generated by Django 5.1.6 on 2025-03-06 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Booking", "0002_booking_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("upcoming", "Upcoming"),
                    ("completed", "Completed"),
                    ("canceled", "Canceled"),
                ],
                default="upcoming",
                max_length=20,
            ),
        ),
    ]

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', 'Upcoming'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled')
        ],
        default='upcoming'
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email}"
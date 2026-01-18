from django.db import models
from django.conf import settings

class Seat(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
    ]

    number = models.PositiveIntegerField(unique=True, help_text="Seat number")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text="Current status of the seat"
    )
    photo = models.ImageField(
        upload_to='seats/',
        blank=True,
        null=True,
        help_text="Photo of the seat"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Seat {self.number} - {self.status}"

    @property
    def is_available(self):
        return self.status == 'available'


class SeatBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    PLAN_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seat_bookings',
        help_text="User who made the booking",
        null=True,  # Temporarily allow null for testing
        blank=True
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Seat being booked"
    )
    start_time = models.DateTimeField(help_text="Booking start time")
    end_time = models.DateTimeField(help_text="Booking end time")
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        help_text="Booking plan type"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        help_text="Payment method used"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Booking status"
    )
    payment_screenshot = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True,
        help_text="Payment screenshot for online payments"
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Transaction ID from payment gateway"
    )
    payment_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Payment ID from payment system"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total booking amount"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Removed unique_together constraint - using application-level validation instead

    def __str__(self):
        return f"Booking for Seat {self.seat.number} by {self.user.username} ({self.status})"

    def save(self, *args, **kwargs):
        # Calculate total amount based on plan and duration
        if not self.total_amount:
            self.total_amount = self.calculate_amount()
        super().save(*args, **kwargs)

    def calculate_amount(self):
        """Calculate booking amount based on plan and duration"""
        duration_hours = (self.end_time - self.start_time).total_seconds() / 3600

        # Pricing logic (you can customize this)
        if self.plan == 'hourly':
            rate_per_hour = 10.00  # ₹10 per hour
            return duration_hours * rate_per_hour
        elif self.plan == 'daily':
            rate_per_day = 50.00  # ₹50 per day
            return (duration_hours / 24) * rate_per_day
        elif self.plan == 'monthly':
            rate_per_month = 500.00  # ₹500 per month
            return (duration_hours / (24 * 30)) * rate_per_month
        else:
            return 0.00
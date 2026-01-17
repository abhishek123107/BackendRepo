from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User
from payments.models import Payment # Payment model import करें

class Room(models.Model):
    """Library room or zone containing seats"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    floor = models.IntegerField(default=1)
    capacity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    amenities = models.JSONField(default=list, blank=True)  # List of amenities like wifi, power, etc.
    operating_hours = models.JSONField(default=dict, blank=True)  # Opening/closing times

    class Meta:
        db_table = 'rooms'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"{self.name} (Floor {self.floor})"

    def update_capacity(self):
        """Update room capacity based on active seats"""
        self.capacity = self.seats.filter(is_active=True).count()
        self.save()


class Seat(models.Model):
    """Individual seat in the library"""

    SEAT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
        ('group', 'Group Study'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)  # e.g., "A01", "B15"
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES, default='regular')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # Physical properties
    has_power_outlet = models.BooleanField(default=False)
    has_monitor = models.BooleanField(default=False)
    is_near_window = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False)  # Wheelchair accessible

    # Administrative
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'seats'
        unique_together = ['room', 'seat_number']
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'

    def __str__(self):
        return f"{self.room.name} - {self.seat_number}"

    def clean(self):
        """Validate seat data"""
        if not self.seat_number:
            raise ValidationError("Seat number is required")

    def is_available_for_booking(self, start_time, end_time):
        """Check if seat is available for the given time period"""
        if self.status != 'available':
            return False

        # Check for conflicting bookings
        conflicting_bookings = SeatBooking.objects.filter(
            seat=self,
            status__in=['confirmed', 'active'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        return not conflicting_bookings.exists()

    def get_current_booking(self):
        """Get the current active booking for this seat"""
        now = timezone.now()
        return SeatBooking.objects.filter(
            seat=self,
            status='active',
            start_time__lte=now,
            end_time__gt=now
        ).first()


class SeatBooking(models.Model):
    """Seat booking records"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, related_name='seat_bookings') # नया payment field

    # Booking details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.FloatField()  # Calculated field

    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)

    # Additional info
    purpose = models.CharField(max_length=100, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    checked_out_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'seat_bookings'
        ordering = ['-created_at']
        verbose_name = 'Seat Booking'
        verbose_name_plural = 'Seat Bookings'

    def __str__(self):
        return f"{self.user.email} - {self.seat} ({self.start_time.date()})"

    def clean(self):
        """Validate booking data"""
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

        if self.start_time < timezone.now():
            raise ValidationError("Cannot book seats in the past")

        # Calculate duration
        duration = self.end_time - self.start_time
        self.duration_hours = duration.total_seconds() / 3600

        # Check for conflicts
        if not self.seat.is_available_for_booking(self.start_time, self.end_time):
            raise ValidationError("Seat is not available for the selected time period")

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate unique booking reference
            import uuid
            self.booking_reference = f"LB{uuid.uuid4().hex[:8].upper()}"

        # Calculate duration if not set
        if not hasattr(self, 'duration_hours') or not self.duration_hours:
            duration = self.end_time - self.start_time
            self.duration_hours = duration.total_seconds() / 3600

        super().save(*args, **kwargs)

    def check_in(self):
        """Mark user as checked in"""
        if self.status == 'confirmed' and self.start_time <= timezone.now() <= self.end_time:
            self.status = 'active'
            self.checked_in_at = timezone.now()
            self.save()

    def check_out(self):
        """Mark user as checked out"""
        if self.status == 'active':
            self.status = 'completed'
            self.checked_out_at = timezone.now()
            self.save()

    def cancel(self):
        """Cancel the booking"""
        if self.status in ['pending', 'confirmed']:
            self.status = 'cancelled'
            self.save()

    @property
    def is_active_now(self):
        """Check if booking is currently active"""
        now = timezone.now()
        return (self.status == 'active' and
                self.start_time <= now <= self.end_time)

    @property
    def is_overdue(self):
        """Check if booking is overdue (past end time but not checked out)"""
        now = timezone.now()
        return (self.status == 'active' and
                now > self.end_time)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from seats.models import SeatBooking
from attendance.models import AttendanceRecord
from .models import User


@receiver(post_save, sender=SeatBooking)
@receiver(post_delete, sender=SeatBooking)
def update_user_booking_stats(sender, instance, **kwargs):
    """Update user's total bookings count"""
    user = instance.user
    completed_bookings = SeatBooking.objects.filter(
        user=user,
        status__in=['completed', 'active']
    ).count()
    user.total_bookings = completed_bookings
    user.save(update_fields=['total_bookings'])


@receiver(post_save, sender=AttendanceRecord)
@receiver(post_delete, sender=AttendanceRecord)
def update_user_attendance_stats(sender, instance, **kwargs):
    """Update user's attendance statistics"""
    user = instance.user

    # Calculate total attendance hours from all records
    attendance_records = AttendanceRecord.objects.filter(
        user=user,
        status__in=['present', 'late']
    )

    total_minutes = attendance_records.aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    user.total_attendance_hours = total_minutes / 60  # Convert to hours

    # Calculate consistency score (percentage of sessions attended)
    total_sessions = AttendanceRecord.objects.filter(user=user).count()
    attended_sessions = attendance_records.count()

    if total_sessions > 0:
        user.consistency_score = (attended_sessions / total_sessions) * 100
    else:
        user.consistency_score = 0.0

    user.save(update_fields=['total_attendance_hours', 'consistency_score'])
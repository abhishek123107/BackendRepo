from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User
from seats.models import SeatBooking
import qrcode
import io
import base64


class AttendanceSession(models.Model):
    """Study session or class period for attendance tracking"""

    SESSION_TYPE_CHOICES = [
        ('study', 'Study Session'),
        ('class', 'Class Period'),
        ('exam', 'Exam Period'),
        ('event', 'Library Event'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='study')

    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    check_in_deadline = models.DateTimeField(blank=True, null=True)  # Optional deadline for check-in

    # Location (optional - can be linked to room)
    # Note: Room model not implemented yet, commenting out for now
    # room = models.ForeignKey('seats.Room', on_delete=models.SET_NULL, blank=True, null=True, related_name='sessions')

    # Session details
    instructor = models.CharField(max_length=100, blank=True, null=True)
    max_participants = models.IntegerField(blank=True, null=True)
    is_mandatory = models.BooleanField(default=False)

    # QR Code for attendance
    qr_code_data = models.TextField(blank=True, null=True)  # Base64 encoded QR code image
    qr_code_token = models.CharField(max_length=100, unique=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_sessions')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_sessions'
        ordering = ['-start_time']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'

    def __str__(self):
        return f"{self.title} - {self.start_time.date()}"

    def clean(self):
        """Validate session data"""
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

        if self.check_in_deadline and self.check_in_deadline > self.end_time:
            raise ValidationError("Check-in deadline cannot be after session end time")

    def save(self, *args, **kwargs):
        if not self.qr_code_token:
            # Generate unique token for QR code
            import uuid
            self.qr_code_token = f"ATT{uuid.uuid4().hex[:12].upper()}"

        # Generate QR code if not exists
        if not self.qr_code_data:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """Generate QR code for attendance check-in"""
        qr_data = f"attendance:{self.qr_code_token}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        self.qr_code_data = f"data:image/png;base64,{img_str}"

    def get_attendance_stats(self):
        """Get attendance statistics for this session"""
        total_records = self.attendance_records.count()
        present_count = self.attendance_records.filter(status='present').count()
        late_count = self.attendance_records.filter(status='late').count()
        absent_count = self.attendance_records.filter(status='absent').count()

        return {
            'total_registered': total_records,
            'present': present_count,
            'late': late_count,
            'absent': absent_count,
            'attendance_rate': (present_count / total_records * 100) if total_records > 0 else 0
        }

    @property
    def is_ongoing(self):
        """Check if session is currently ongoing"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def has_ended(self):
        """Check if session has ended"""
        return timezone.now() > self.end_time


class AttendanceRecord(models.Model):
    """Individual attendance record for a user in a session"""

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='attendance_records')

    # Attendance details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=0)  # Time spent in minutes

    # Additional info
    notes = models.TextField(blank=True, null=True)
    seat_booking = models.ForeignKey(SeatBooking, on_delete=models.SET_NULL, blank=True, null=True, related_name='attendance')

    # Verification
    verified_by_qr = models.BooleanField(default=False)
    verification_method = models.CharField(max_length=50, blank=True, null=True)  # 'qr_code', 'manual', 'auto'

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance_records'
        unique_together = ['user', 'session']
        ordering = ['-created_at']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.user.email} - {self.session.title} ({self.status})"

    def save(self, *args, **kwargs):
        # Calculate duration if both times are set
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time
            self.duration_minutes = int(duration.total_seconds() / 60)
        super().save(*args, **kwargs)

    def mark_present(self, check_in_time=None):
        """Mark user as present"""
        now = check_in_time or timezone.now()
        self.status = 'present'
        self.check_in_time = now

        # Check if late
        if self.session.check_in_deadline and now > self.session.check_in_deadline:
            self.status = 'late'

        self.save()

    def check_out(self, check_out_time=None):
        """Record check-out time"""
        now = check_out_time or timezone.now()
        self.check_out_time = now

        if self.check_in_time:
            duration = now - self.check_in_time
            self.duration_minutes = int(duration.total_seconds() / 60)

        self.save()

    @property
    def is_checked_in(self):
        """Check if user has checked in"""
        return self.check_in_time is not None

    @property
    def is_checked_out(self):
        """Check if user has checked out"""
        return self.check_out_time is not None

    @property
    def actual_duration(self):
        """Get actual duration spent"""
        if self.check_in_time and self.check_out_time:
            return self.check_out_time - self.check_in_time
        return None


class AttendanceReport(models.Model):
    """Generated attendance reports"""

    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('session', 'Session Report'),
        ('user', 'User Report'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    # Report parameters
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.ForeignKey(AttendanceSession, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='attendance_reports')

    # Report data (stored as JSON)
    report_data = models.JSONField()
    summary = models.JSONField()

    # File storage
    pdf_file = models.FileField(upload_to='attendance_reports/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_reports'
        ordering = ['-created_at']
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'

    def __str__(self):
        return f"{self.title} - {self.report_type} ({self.start_date} to {self.end_date})"

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model for Library Seat Booking System"""

    # Basic user information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # Student specific fields
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('vip', 'VIP'),
        ],
        default='basic'
    )
    membership_expiry = models.DateTimeField(blank=True, null=True)

    # Profile information
    avatar = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    # Statistics
    total_bookings = models.IntegerField(default=0)
    total_attendance_hours = models.IntegerField(default=0)
    consistency_score = models.FloatField(default=0.0)

    # Status
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Required fields for Django
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} - {self.get_full_name() or self.username}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def is_membership_active(self):
        """Check if user has active membership"""
        if not self.membership_expiry:
            return False
        return self.membership_expiry > timezone.now()

    def update_statistics(self):
        """Update user statistics based on bookings and attendance"""
        # This will be called after booking/attendance operations
        self.total_bookings = self.bookings.count()
        self.total_attendance_hours = self.attendances.filter(status='present').count()
        # Calculate consistency score (percentage of attended sessions)
        total_sessions = self.attendances.count()
        if total_sessions > 0:
            attended_sessions = self.attendances.filter(status='present').count()
            self.consistency_score = (attended_sessions / total_sessions) * 100
        self.save()


class UserProfile(models.Model):
    """Extended user profile information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    interests = models.JSONField(default=list, blank=True)  # Store as list of interests
    preferred_study_times = models.JSONField(default=list, blank=True)  # Store preferred time slots
    notifications_enabled = models.BooleanField(default=True)
    theme_preference = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile for {self.user.email}"

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

class MembershipPlan(models.Model):
    """लाइब्रेरी एक्सेस के लिए सदस्यता योजनाएं"""
    PLAN_TYPE_CHOICES = [
        ('morning_shift', 'Morning Shift (6 AM - 11 AM)'),
        ('afternoon_shift', 'Afternoon Shift (11 AM - 4 PM)'),
        ('evening_shift', 'Evening Shift (4 PM - 9 PM)'),
        ('full_day', 'Full Day (12 Hours)'),
        ('night_shift', 'Night Shift (7 PM - 6 AM)'),
        ('24_7_access', '24/7 Access (Unlimited)'),
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    
    # Shift timing details
    start_time = models.TimeField(blank=True, null=True)  # For shift-based plans
    end_time = models.TimeField(blank=True, null=True)    # For shift-based plans

    # विशेषताएं
    max_bookings_per_day = models.IntegerField(default=1)
    priority_booking = models.BooleanField(default=False)
    extended_hours = models.BooleanField(default=False)
    
    # Amenities included
    includes_personal_charging = models.BooleanField(default=True)
    includes_led_lighting = models.BooleanField(default=True)
    includes_ro_water = models.BooleanField(default=True)
    includes_wifi = models.BooleanField(default=True)
    includes_ac = models.BooleanField(default=True)
    includes_comfortable_chairs = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'membership_plans'
        verbose_name = 'Membership Plan'
        verbose_name_plural = 'Membership Plans'

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Payment(models.Model):
    """सदस्यता और बुकिंग के लिए पेमेंट रिकॉर्ड (Screenshot और Admin Approval के साथ)"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    # संबंध
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, blank=True, null=True, related_name='payments')

    # मुख्य विवरण
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, default='online') # 'online' या 'offline'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # प्रूफ और ट्रांजैक्शन विवरण (मैनुअल पेमेंट के लिए)
    transaction_id = models.CharField(max_length=100, unique=True)
    account_holder_name = models.CharField(max_length=100)
    screenshot = models.ImageField(upload_to='payment_proofs/')
    
    # तिथियां
    date = models.DateField() # यूजर द्वारा भरी गई पेमेंट की तारीख
    created_at = models.DateTimeField(auto_now_add=True) # सिस्टम एंट्री टाइम

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} ({self.status})"

    def clean(self):
        """पेमेंट डेटा की वैधता जांचें"""
        if self.amount <= 0:
            raise ValidationError("Payment amount must be positive")

    def save(self, *args, **kwargs):
        # अगर एडमिन स्टेटस 'paid' करता है और प्लान जुड़ा है, तो यूजर की एक्सपायरी अपडेट करें
        if self.pk:
            old_status = Payment.objects.get(pk=self.pk).status
            if old_status != 'paid' and self.status == 'paid' and self.membership_plan:
                self.update_user_membership()
        super().save(*args, **kwargs)

    def update_user_membership(self):
        """यूजर की सदस्यता अपडेट करें"""
        user = self.user
        user.membership_type = self.membership_plan.plan_type
        user.membership_expiry = timezone.now() + timezone.timedelta(days=self.membership_plan.duration_days)
        user.save()
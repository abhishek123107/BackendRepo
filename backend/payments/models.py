from django.db import models
from django.contrib.auth.models import User


class PaymentRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_records',
        help_text="User who made the payment"
    )
    description = models.CharField(
        max_length=200,
        help_text="Payment description (e.g., Membership Fee)"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Payment amount"
    )
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        help_text="Payment method"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Payment status"
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Transaction ID from payment gateway"
    )
    account_holder_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Account holder name"
    )
    date = models.DateField(
        help_text="Payment date"
    )
    screenshot = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True,
        help_text="Payment screenshot"
    )
    membership_plan = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Membership plan ID if applicable"
    )
    plan_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Plan name"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.amount} by {self.user.username} ({self.status})"

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - read-only, returns all user fields"""

    full_name = serializers.SerializerMethodField()
    membership_status = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'full_name', 'student_id', 'membership_type', 'membership_expiry',
            'membership_status', 'days_until_expiry', 'avatar', 'department',
            'year_of_study', 'total_bookings', 'total_attendance_hours',
            'consistency_score', 'is_active', 'date_joined', 'is_staff', 'is_superuser'
        ]
        read_only_fields = [
            'id', 'date_joined', 'total_bookings', 'total_attendance_hours',
            'consistency_score', 'is_staff', 'is_superuser'
        ]

    def get_full_name(self, obj):
        """Get full name of user"""
        return obj.get_full_name() or obj.username

    def get_membership_status(self, obj):
        """Get current membership status"""
        if not obj.membership_expiry:
            return 'No Active Membership'

        now = timezone.now()
        return 'Active' if obj.membership_expiry > now else 'Expired'

    def get_days_until_expiry(self, obj):
        """Get days until membership expires"""
        if not obj.membership_expiry:
            return None

        now = timezone.now()
        return (obj.membership_expiry - now).days if obj.membership_expiry > now else 0


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration - validates and creates new users"""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Password is required',
            'blank': 'Password cannot be blank',
            'min_length': 'Password must be at least 8 characters long'
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Password confirmation is required',
            'blank': 'Password confirmation cannot be blank'
        }
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'password', 'password_confirm',
            'first_name', 'last_name', 'student_id', 'department', 'year_of_study'
        ]
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_username(self, value):
        """Validate username is unique and not blank"""
        if not value or not value.strip():
            raise serializers.ValidationError('Username is required')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value.strip()

    def validate_email(self, value):
        """Validate email is valid and unique"""
        if not value or not value.strip():
            raise serializers.ValidationError('Email is required')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value.strip()

    def validate(self, data):
        """Validate passwords match and phone is unique"""
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })

        phone = data.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({
                'phone': 'Phone number already registered'
            })

        return data

    def create(self, validated_data):
        """Create new user with validated data"""
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login - validates credentials"""

    email_or_phone = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Email or phone number is required',
            'blank': 'Email or phone number cannot be blank'
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        allow_blank=False,
        error_messages={
            'required': 'Password is required',
            'blank': 'Password cannot be blank'
        }
    )

    def validate_email_or_phone(self, value):
        """Validate that email_or_phone is provided"""
        if not value or not value.strip():
            raise serializers.ValidationError('Email or phone number is required')
        return value.strip()

    def validate_password(self, value):
        """Validate that password is provided"""
        if not value or not value.strip():
            raise serializers.ValidationError('Password is required')
        return value

    def validate(self, data):
        """Authenticate user with email/phone and password"""
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')

        if not email_or_phone or not password:
            raise serializers.ValidationError({
                'detail': 'Email/Phone and password are required'
            })

        user = None

        # Try to find user by email first (since USERNAME_FIELD = 'email')
        try:
            user_obj = User.objects.get(email=email_or_phone)
            user = authenticate(username=user_obj.email, password=password)
        except User.DoesNotExist:
            pass

        if not user:
            # Try to find user by phone
            try:
                user_obj = User.objects.get(phone=email_or_phone)
                user = authenticate(username=user_obj.email, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            # Try to find user by username (fallback)
            try:
                user_obj = User.objects.get(username=email_or_phone)
                user = authenticate(username=user_obj.email, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError({'detail': ['Invalid credentials']})

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError({'detail': ['Account is disabled']})

        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={
            'min_length': 'New password must be at least 8 characters long'
        }
    )
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        """Validate password change data"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'New passwords do not match'
            })

        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': 'New password must be different from old password'
            })

        return data
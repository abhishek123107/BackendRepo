from rest_framework import serializers
from .models import Seat, SeatBooking
from django.contrib.auth.models import User


class SeatSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        # Return a default placeholder URL using picsum.photos which is more reliable
        return f'https://picsum.photos/seed/seat{obj.number}/400/300.jpg'

    class Meta:
        model = Seat
        fields = ['id', 'number', 'status', 'photo']


class SeatBookingSerializer(serializers.ModelSerializer):
    seat_number = serializers.ReadOnlyField(source='seat.number')

    class Meta:
        model = SeatBooking
        fields = [
            'id', 'user', 'seat', 'seat_number', 'start_time', 'end_time',
            'plan', 'payment_method', 'status', 'payment_screenshot',
            'transaction_id', 'payment_id', 'total_amount', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set user from request context if not provided
        if 'user' not in validated_data:
            request = self.context.get('request')
            if request and request.user and request.user.is_authenticated:
                validated_data['user'] = request.user
            else:
                # For testing: create a dummy user or skip user requirement
                # In production, this should require authentication
                pass
        return super().create(validated_data)


class SeatBookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings (with file upload support)"""

    class Meta:
        model = SeatBooking
        fields = [
            'seat', 'start_time', 'end_time', 'plan', 'payment_method',
            'payment_screenshot', 'transaction_id', 'payment_id'
        ]
        extra_kwargs = {
            'payment_method': {'required': False, 'default': 'offline'},
            'payment_screenshot': {'required': False},
            'transaction_id': {'required': False},
            'payment_id': {'required': False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make payment_screenshot required for online payments
        if hasattr(self, 'context') and self.context.get('request'):
            request = self.context['request']
            payment_method = request.data.get('payment_method') if hasattr(request.data, 'get') else request.data.get('payment_method')
            if payment_method == 'online':
                self.fields['payment_screenshot'].required = True

    def to_internal_value(self, data):
        """Handle field name mapping from frontend to backend"""
        # Convert 'purpose' to 'plan' if present
        if 'purpose' in data and 'plan' not in data:
            data = data.copy()  # Create a mutable copy for FormData
            data['plan'] = data['purpose']
            del data['purpose']

        return super().to_internal_value(data)

    def validate(self, data):
        # Additional validation
        payment_method = data.get('payment_method', 'offline')

        if payment_method == 'online' and not data.get('payment_screenshot'):
            raise serializers.ValidationError({
                'payment_screenshot': 'Payment screenshot is required for online payments.'
            })

        return data

    def create(self, validated_data):
        # Set user from request context only if authenticated
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            # For anonymous users, don't set user (it's nullable)
            validated_data.pop('user', None)
        return super().create(validated_data)
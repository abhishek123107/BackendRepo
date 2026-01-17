from rest_framework import serializers
from django.utils import timezone
from .models import Room, Seat, SeatBooking
from payments.serializers import PaymentSerializer


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""

    seat_count = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'name', 'description', 'floor', 'capacity',
            'amenities', 'operating_hours', 'is_active',
            'seat_count', 'available_seats'
        ]

    def get_seat_count(self, obj):
        return obj.seats.filter(is_active=True).count()

    def get_available_seats(self, obj):
        return obj.seats.filter(is_active=True, status='available').count()


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model"""

    room_name = serializers.SerializerMethodField()
    number = serializers.CharField(source='seat_number', read_only=True)  # Map seat_number to number for frontend compatibility
    photo = serializers.SerializerMethodField()  # Add photo field for frontend compatibility
    current_booking = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = [
            'id', 'number', 'room', 'room_name', 'seat_number', 'seat_type', 'status',
            'has_power_outlet', 'has_monitor', 'is_near_window', 'is_accessible',
            'is_active', 'notes', 'current_booking', 'photo'
        ]
        read_only_fields = ['id']

    def get_room_name(self, obj):
        """Safely get room name"""
        try:
            if hasattr(obj, 'room') and obj.room:
                return obj.room.name
        except Exception:
            pass
        return None

    def get_photo(self, obj):
        """Return a placeholder photo URL for the seat"""
        try:
            seat_id = getattr(obj, 'id', 0) or 0
            return f'https://picsum.photos/400/300?random={seat_id}'
        except Exception:
            return 'https://picsum.photos/400/300?random=1'

    def to_representation(self, instance):
        """Customize the output to match frontend expectations"""
        # Status mapping defined outside try block for use in exception handler
        status_mapping = {
            'reserved': 'booked',
            'occupied': 'booked',
            'maintenance': 'maintenance',
            'available': 'available'
        }
        
        try:
            # Ensure room is loaded to avoid database queries during serialization
            if hasattr(instance, 'room') and instance.room_id and not hasattr(instance, '_room_cache'):
                try:
                    instance.room  # This will trigger the database query if not already loaded
                except Exception:
                    pass
            
            data = super().to_representation(instance)
            # Map backend status to frontend status
            data['status'] = status_mapping.get(instance.status, 'available')
            # Ensure number field is set correctly
            if 'number' not in data or not data['number']:
                data['number'] = getattr(instance, 'seat_number', '')
            return data
        except Exception as e:
            # Log error but return basic data to prevent 500 error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in SeatSerializer.to_representation for seat {getattr(instance, 'id', 'unknown')}: {str(e)}")
            # Return minimal data to prevent 500 error
            try:
                return {
                    'id': getattr(instance, 'id', None),
                    'number': getattr(instance, 'seat_number', ''),
                    'status': status_mapping.get(getattr(instance, 'status', 'available'), 'available'),
                    'photo': self.get_photo(instance),
                    'room_name': self.get_room_name(instance),
                    'is_active': getattr(instance, 'is_active', True)
                }
            except Exception:
                # Ultimate fallback
                return {
                    'id': None,
                    'number': '',
                    'status': 'available',
                    'photo': 'https://picsum.photos/400/300?random=1'
                }

    def get_current_booking(self, obj):
        """Safely get current booking"""
        try:
            if hasattr(obj, 'get_current_booking'):
                booking = obj.get_current_booking()
                if booking:
                    return {
                        'id': booking.id,
                        'user': booking.user.get_full_name() if hasattr(booking.user, 'get_full_name') else (booking.user.username if hasattr(booking.user, 'username') else None),
                        'start_time': booking.start_time.isoformat() if hasattr(booking.start_time, 'isoformat') else str(booking.start_time),
                        'end_time': booking.end_time.isoformat() if hasattr(booking.end_time, 'isoformat') else str(booking.end_time)
                    }
        except Exception:
            pass
        return None


class SeatBookingSerializer(serializers.ModelSerializer):
    """Serializer for SeatBooking model"""

    user_name = serializers.SerializerMethodField()
    seat_details = SeatSerializer(source='seat', read_only=True)
    can_cancel = serializers.SerializerMethodField()
    can_check_in = serializers.SerializerMethodField()
    can_check_out = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()

    class Meta:
        model = SeatBooking
        fields = [
            'id', 'user', 'user_name', 'seat', 'seat_details',
            'start_time', 'end_time', 'duration_hours', 'status',
            'booking_reference', 'purpose', 'special_requests',
            'payment', 'payment_details',
            'created_at', 'updated_at', 'checked_in_at', 'checked_out_at',
            'can_cancel', 'can_check_in', 'can_check_out'
        ]
        read_only_fields = [
            'id', 'user', 'duration_hours', 'booking_reference',
            'created_at', 'updated_at', 'checked_in_at', 'checked_out_at'
        ]

    def get_user_name(self, obj):
        try:
            if hasattr(obj, 'user') and obj.user:
                return obj.user.get_full_name() or obj.user.username
        except Exception:
            pass
        return None

    def get_payment_details(self, obj):
        """Safely get payment details"""
        try:
            if hasattr(obj, 'payment') and obj.payment:
                return PaymentSerializer(obj.payment).data
        except Exception:
            pass
        return None

    def get_can_cancel(self, obj):
        return obj.status in ['pending', 'confirmed']

    def get_can_check_in(self, obj):
        now = timezone.now()
        return (obj.status == 'confirmed' and
                obj.start_time <= now <= obj.end_time)

    def get_can_check_out(self, obj):
        return obj.status == 'active'

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        seat = data.get('seat')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time")

            if start_time < timezone.now():
                raise serializers.ValidationError("Cannot book seats in the past")

            # Check availability
            if seat and not seat.is_available_for_booking(start_time, end_time):
                raise serializers.ValidationError("Seat is not available for the selected time period")

        return data


class SeatBookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating seat bookings with file upload support"""
    payment_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    payment_screenshot = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = SeatBooking
        fields = [
            'seat', 'start_time', 'end_time', 'purpose', 'special_requests',
            'payment_id', 'payment_screenshot'
        ]

    def validate(self, data):
        # #region agent log - Entry point
        import json
        import os
        log_file = None
        try:
            # Calculate log file path: go up from seats/serializers.py -> seats -> library_booking_api -> LibrarySeatBooking -> .cursor
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            log_dir = os.path.join(base_dir, '.cursor')
            os.makedirs(log_dir, exist_ok=True)  # Ensure directory exists
            log_file = os.path.join(log_dir, 'debug.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"location": "serializers.py:212", "message": "validate method called", "data": {"data_keys": list(data.keys()) if hasattr(data, 'keys') else None, "start_time_raw": str(data.get('start_time')) if data.get('start_time') else None, "start_time_type": str(type(data.get('start_time'))) if data.get('start_time') else None, "end_time_raw": str(data.get('end_time')) if data.get('end_time') else None, "end_time_type": str(type(data.get('end_time'))) if data.get('end_time') else None}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
        except Exception as e:
            # Log to a fallback location if main log fails
            try:
                fallback_log = os.path.join(os.path.dirname(__file__), 'debug_fallback.log')
                with open(fallback_log, 'a', encoding='utf-8') as f:
                    f.write(f"Log error: {str(e)}\n")
            except:
                pass
        # #endregion
        
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        seat = data.get('seat')
        payment_id = data.get('payment_id')
        payment_screenshot = data.get('payment_screenshot')

        # Parse datetime strings if they're still strings (FormData sends strings)
        from django.utils.dateparse import parse_datetime
        
        if isinstance(start_time, str):
            # #region agent log
            if log_file:
                try:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"location": "serializers.py:222", "message": "start_time is string, parsing", "data": {"start_time_str": start_time}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
                except Exception:
                    pass
            # #endregion
            parsed = parse_datetime(start_time)  # parse_datetime handles 'Z' suffix natively
            if parsed:
                if not timezone.is_aware(parsed):
                    parsed = timezone.make_aware(parsed, timezone.utc)
                start_time = parsed
                data['start_time'] = start_time
                # #region agent log
                if log_file:
                    try:
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(json.dumps({"location": "serializers.py:230", "message": "start_time parsed successfully", "data": {"parsed_value": str(parsed), "is_aware": timezone.is_aware(parsed), "iso": parsed.isoformat()}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
                    except Exception:
                        pass
                # #endregion
            else:
                # #region agent log
                if log_file:
                    try:
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(json.dumps({"location": "serializers.py:236", "message": "parse_datetime failed for start_time", "data": {"start_time_str": start_time}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
                    except Exception:
                        pass
                # #endregion
                raise serializers.ValidationError({"start_time": "Invalid datetime format"})
        elif start_time and not timezone.is_aware(start_time):
            # If it's a datetime but naive, make it aware
            # #region agent log
            if log_file:
                try:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"location": "serializers.py:243", "message": "start_time is naive datetime, making aware", "data": {"start_time_value": str(start_time)}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
                except Exception:
                    pass
            # #endregion
            start_time = timezone.make_aware(start_time, timezone.utc)
            data['start_time'] = start_time
        elif start_time:
            # #region agent log
            if log_file:
                try:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"location": "serializers.py:250", "message": "start_time is already datetime", "data": {"start_time_value": str(start_time), "is_aware": timezone.is_aware(start_time), "type": str(type(start_time))}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "J"}) + "\n")
                except Exception:
                    pass
            # #endregion
        
        if isinstance(end_time, str):
            parsed = parse_datetime(end_time)  # parse_datetime handles 'Z' suffix natively
            if parsed:
                if not timezone.is_aware(parsed):
                    parsed = timezone.make_aware(parsed, timezone.utc)
                end_time = parsed
                data['end_time'] = end_time
            else:
                raise serializers.ValidationError({"end_time": "Invalid datetime format"})
        elif end_time and not timezone.is_aware(end_time):
            # If it's a datetime but naive, make it aware
            end_time = timezone.make_aware(end_time, timezone.utc)
            data['end_time'] = end_time

        if start_time and end_time:
            # #region agent log
            now = timezone.now()
            if log_file:
                try:
                    log_data = {
                        "start_time_type": str(type(start_time)),
                        "start_time_value": str(start_time),
                        "start_time_iso": start_time.isoformat() if hasattr(start_time, 'isoformat') else None,
                        "start_time_tzaware": timezone.is_aware(start_time) if hasattr(timezone, 'is_aware') else None,
                        "now_value": str(now),
                        "now_iso": now.isoformat(),
                        "comparison_result": start_time < now,
                        "time_diff_seconds": (now - start_time).total_seconds() if hasattr(now - start_time, 'total_seconds') else None
                    }
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"location": "serializers.py:212", "message": "validate start_time check", "data": log_data, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "G"}) + "\n")
                except Exception:
                    pass
            # #endregion
            
            if start_time >= end_time:
                raise serializers.ValidationError({"end_time": "End time must be after start time"})
            
            # Final comparison with current time
            # Add a 1-minute buffer to account for timezone differences and clock skew
            from datetime import timedelta
            now = timezone.now()
            buffer_time = now - timedelta(minutes=1)  # Allow times up to 1 minute in the past
            
            # Only reject if start_time is more than 1 minute in the past
            if start_time < buffer_time:
                # Calculate time difference for better error message
                time_diff = (now - start_time).total_seconds()
                raise serializers.ValidationError({
                    "start_time": f"Cannot book seats in the past. Start time is {int(time_diff/60)} minutes ago."
                })
            # If within 1 minute buffer or in the future, allow it

            # Check availability
            if seat and not seat.is_available_for_booking(start_time, end_time):
                raise serializers.ValidationError({"seat": "Seat is not available for the selected time period"})

        # Payment validation - if payment_screenshot is provided, it's an online payment
        if payment_screenshot:
            # Online payment with screenshot - this is valid
            pass
        elif payment_id:
            # Payment ID validation
            from payments.models import Payment
            try:
                payment = Payment.objects.get(id=payment_id)
                if payment.status != 'pending':
                    raise serializers.ValidationError({"payment_id": "Invalid payment status for booking."})
            except Payment.DoesNotExist:
                raise serializers.ValidationError({"payment_id": "Payment not found."})

        return data

    def create(self, validated_data):
        payment_id = validated_data.pop('payment_id', None)
        payment_screenshot = validated_data.pop('payment_screenshot', None)
        
        # Create booking first
        booking = SeatBooking.objects.create(**validated_data)
        
        # Handle payment association
        if payment_id:
            from payments.models import Payment
            try:
                payment = Payment.objects.get(id=payment_id)
                booking.payment = payment
                booking.save()
            except Payment.DoesNotExist:
                # If payment doesn't exist, we still have the booking
                pass
        
        # If payment screenshot is provided but no payment_id, create a payment record
        elif payment_screenshot:
            from payments.models import Payment
            from django.contrib.auth.models import User
            from django.utils import timezone
            
            # Create a payment record from the screenshot
            payment = Payment.objects.create(
                user=booking.user,
                description=f"Seat Booking - {booking.seat}",
                amount=0,  # Will be updated by admin
                method='online',
                status='pending',
                screenshot=payment_screenshot,
                date=timezone.now().date()  # Add required date field
            )
            booking.payment = payment
            booking.save()
        
        return booking

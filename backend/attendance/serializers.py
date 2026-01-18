from rest_framework import serializers
from .models import AttendanceSession, AttendanceRecord


class AttendanceSessionSerializer(serializers.ModelSerializer):
    """Serializer for AttendanceSession model"""

    qr_code_url = serializers.SerializerMethodField()
    attendance_count = serializers.SerializerMethodField()
    is_active_now = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = [
            'id', 'title', 'description', 'session_type', 'start_time', 'end_time',
            'check_in_deadline', 'room', 'instructor', 'max_participants',
            'is_mandatory', 'qr_code_data', 'qr_code_token', 'is_active',
            'created_by', 'created_at', 'qr_code_url', 'attendance_count', 'is_active_now'
        ]
        read_only_fields = ['id', 'qr_code_data', 'qr_code_token', 'created_at']

    def get_qr_code_url(self, obj):
        if obj.qr_code_data:
            return f"data:image/png;base64,{obj.qr_code_data}"
        return None

    def get_attendance_count(self, obj):
        return obj.records.count()

    def get_is_active_now(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.start_time <= now <= obj.end_time


class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializer for AttendanceRecord model"""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    session_title = serializers.CharField(source='session.title', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'session', 'session_title', 'user', 'user_name',
            'check_in_time', 'check_out_time', 'duration_minutes',
            'method', 'marked_by', 'marked_by_name', 'notes'
        ]
        read_only_fields = ['id', 'check_in_time', 'check_out_time', 'duration_minutes']


class AttendanceSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating attendance sessions"""

    class Meta:
        model = AttendanceSession
        fields = [
            'title', 'description', 'session_type', 'start_time', 'end_time',
            'check_in_deadline', 'room', 'instructor', 'max_participants',
            'is_mandatory'
        ]

    def create(self, validated_data):
        # Generate QR token
        import uuid
        validated_data['qr_token'] = str(uuid.uuid4())[:8].upper()

        # Generate QR code
        qr_data = f"attendance:{validated_data['qr_token']}"
        import qrcode
        import io
        import base64

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()

        validated_data['qr_code_data'] = qr_code_data

        return super().create(validated_data)
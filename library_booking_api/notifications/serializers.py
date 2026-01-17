from rest_framework import serializers
from .models import Notification, UserNotification

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'type', 'target_audience', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserNotificationSerializer(serializers.ModelSerializer):
    """Serializer for UserNotification model"""
    notification = NotificationSerializer(read_only=True)
    
    class Meta:
        model = UserNotification
        fields = [
            'id', 'user', 'notification', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

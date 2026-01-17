from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, UserNotification
from .serializers import NotificationSerializer, UserNotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification model (admin only)"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Only staff can manage notifications"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated]
        return [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Filter notifications based on user role"""
        user = self.request.user
        if user.is_staff:
            return Notification.objects.all()
        else:
            # Non-staff users can only see active notifications
            return Notification.objects.filter(is_active=True)

class UserNotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for UserNotification model"""
    serializer_class = UserNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the current user"""
        user = self.request.user
        return UserNotification.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Automatically set the user to current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Get notifications for the current user"""
        user = request.user
        
        # Get all active notifications that apply to this user
        applicable_notifications = []
        for notification in Notification.objects.filter(is_active=True):
            if notification.get_for_user(user):
                # Get or create UserNotification for this user and notification
                user_notification, created = UserNotification.objects.get_or_create(
                    user=user,
                    notification=notification
                )
                applicable_notifications.append(user_notification)
        
        # Sort by creation date
        applicable_notifications.sort(key=lambda x: x.created_at, reverse=True)
        
        serializer = self.get_serializer(applicable_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read"""
        user_notification = self.get_object()
        user_notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})

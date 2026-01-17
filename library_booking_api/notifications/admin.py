from django.contrib import admin
from .models import Notification, UserNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'target_audience', 'is_active', 'created_at']
    list_filter = ['type', 'target_audience', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification', 'is_read', 'read_at', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'notification__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

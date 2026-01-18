from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin interface for User model with student details"""
    
    list_display = (
        'username', 'email', 'full_name', 'phone', 'student_id', 
        'department', 'year_of_study', 'membership_type', 
        'membership_status', 'total_bookings', 'is_active'
    )
    
    list_filter = (
        'membership_type', 'department', 'year_of_study', 
        'is_active', 'is_staff', 'date_joined'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 'phone')
    
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone')
        }),
        ('Student Details', {
            'fields': ('student_id', 'department', 'year_of_study')
        }),
        ('Membership Information', {
            'fields': ('membership_type', 'membership_expiry')
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'total_attendance_hours', 'consistency_score'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('date_joined', 'last_login', 'total_bookings', 'total_attendance_hours', 'consistency_score')
    
    # Add custom actions for bulk operations
    actions = ['activate_users', 'deactivate_users', 'upgrade_membership']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    full_name.short_description = 'Full Name'
    
    def membership_status(self, obj):
        if not obj.membership_expiry:
            return format_html('<span style="color: red;">No Active Membership</span>')
        
        from django.utils import timezone
        now = timezone.now()
        if obj.membership_expiry > now:
            return format_html('<span style="color: green;">Active</span>')
        else:
            return format_html('<span style="color: red;">Expired</span>')
    membership_status.short_description = 'Membership Status'
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} users activated successfully.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} users deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def upgrade_membership(self, request, queryset):
        queryset.update(membership_type='premium')
        self.message_user(request, f'{queryset.count()} users upgraded to premium membership.')
    upgrade_membership.short_description = 'Upgrade to Premium'
    
    # Show only regular users (not staff) by default
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_staff=False, is_superuser=False)
    
    # Add dashboard statistics
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Calculate statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        student_users = User.objects.filter(is_staff=False, is_superuser=False).count()
        premium_members = User.objects.filter(membership_type='premium').count()
        
        extra_context['dashboard_stats'] = {
            'total_users': total_users,
            'active_users': active_users,
            'student_users': student_users,
            'premium_members': premium_members,
        }
        
        return super().changelist_view(request, extra_context)


# Customize admin site header and title
admin.site.site_header = 'Library Seat Booking Administration'
admin.site.site_title = 'Library Admin'
admin.site.index_title = 'Welcome to Library Seat Booking Admin Panel'

from django.contrib import admin
from .models import User, UserProfile

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'student_id', 'membership_type', 'is_staff')
    search_fields = ('email', 'username', 'phone')
    list_filter = ('membership_type', 'is_active')

admin.site.register(UserProfile)
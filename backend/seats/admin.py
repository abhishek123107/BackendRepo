from django.contrib import admin
from .models import Seat, SeatBooking


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['number', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['number']
    ordering = ['number']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ['number', 'created_at']
        return ['created_at']


@admin.register(SeatBooking)
class SeatBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'seat', 'start_time', 'end_time', 'status', 'payment_method', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'plan', 'created_at', 'start_time']
    search_fields = ['user__username', 'seat__number', 'transaction_id']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']

    fieldsets = (
        ('Booking Details', {
            'fields': ('user', 'seat', 'start_time', 'end_time', 'plan', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_screenshot', 'transaction_id', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ['user', 'seat', 'start_time', 'end_time', 'total_amount', 'created_at', 'updated_at']
        return ['total_amount', 'created_at', 'updated_at']
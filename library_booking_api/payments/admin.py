from django.contrib import admin
from django.utils.html import format_html
from .models import MembershipPlan, Payment

# 1. Membership Plan Admin
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'duration_days', 'is_active']
    list_filter = ['is_active', 'plan_type']
    search_fields = ['name']

# 2. Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # वही फ़ील्ड्स जो आपके अपडेटेड Payment मॉडल में हैं
    list_display = ('id', 'user', 'amount', 'date', 'status', 'transaction_id', 'screenshot_tag')
    list_filter = ('status', 'date', 'method')
    search_fields = ('transaction_id', 'account_holder_name', 'user__username', 'user__email')
    
    # readonly_fields: जिन्हें एडमिन नहीं बदल सकता
    readonly_fields = ('created_at', 'screenshot_tag')
    
    ordering = ('-created_at',)
    list_editable = ('status',) # लिस्ट पेज से ही Approve/Reject करने के लिए

    # एडमिन पैनल में इमेज दिखाने का फंक्शन
    def screenshot_tag(self, obj):
        if obj.screenshot:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="50" height="50" style="border:1px solid #d1d1d1; border-radius:5px;"/></a>', obj.screenshot.url)
        return "No Proof"
    
    screenshot_tag.short_description = 'Proof'

    def get_queryset(self, request):
        # डेटाबेस पर लोड कम करने के लिए select_related
        return super().get_queryset(request).select_related('user', 'membership_plan')
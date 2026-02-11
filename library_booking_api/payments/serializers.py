from rest_framework import serializers
from .models import MembershipPlan, Payment

class MembershipPlanSerializer(serializers.ModelSerializer):
    """सदस्यता योजनाओं के लिए Serializer"""
    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'name', 'plan_type', 'price', 'duration_days',
            'description', 'start_time', 'end_time',
            'max_bookings_per_day', 'priority_booking', 'extended_hours',
            'includes_personal_charging', 'includes_led_lighting', 'includes_ro_water',
            'includes_wifi', 'includes_ac', 'includes_comfortable_chairs',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """पेमेंट रिकॉर्ड्स के लिए Serializer (स्क्रीनशॉट और मैनुअल डिटेल्स के साथ)"""
    
    username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')
    plan_name = serializers.ReadOnlyField(source='membership_plan.name')

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'username', 'user_email', 'membership_plan', 'plan_name',
            'description', 'amount', 'method', 'status', 'transaction_id', 
            'account_holder_name', 'screenshot', 'date', 'created_at'
        ]
        # user, status को read_only रखें - user automatically set होगा view में
        read_only_fields = ['id', 'user', 'status', 'created_at']
        extra_kwargs = {
            'screenshot': {'required': False, 'allow_null': True}  # Make screenshot optional
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
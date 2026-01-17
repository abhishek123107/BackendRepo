from rest_framework import serializers
from .models import PaymentRecord


class PaymentRecordSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')
    screenshot = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRecord
        fields = [
            'id', 'user', 'username', 'user_email', 'description', 'amount', 
            'method', 'status', 'transaction_id', 'account_holder_name', 
            'date', 'screenshot', 'membership_plan', 'plan_name', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_screenshot(self, obj):
        if obj.screenshot:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.screenshot.url)
            return obj.screenshot.url
        return None

    def create(self, validated_data):
        # Set user from request context
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

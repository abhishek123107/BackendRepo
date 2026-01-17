from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Sum
from .models import MembershipPlan, Payment
from .serializers import MembershipPlanSerializer, PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class MembershipPlanViewSet(viewsets.ModelViewSet):
    """सदस्यता योजनाओं के लिए ViewSet"""
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PaymentViewSet(viewsets.ModelViewSet):
    """पेमेंट और स्क्रीनशॉट अपलोड हैंडल करने के लिए ViewSet"""
    serializer_class = PaymentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser) # Support both file upload and JSON
    pagination_class = None  # Disable pagination to return list directly

    def get_queryset(self):
        # एडमिन सब देख सकता है, यूजर सिर्फ अपना डेटा
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all().order_by('-created_at')
        return Payment.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        # सेव करते समय लॉगिन यूजर को ऑटोमैटिक जोड़ें
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a payment (admin only)"""
        payment = self.get_object()
        payment.status = 'paid'
        payment.save()
        return Response({'message': 'Payment approved successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a payment (admin only)"""
        payment = self.get_object()
        payment.status = 'rejected'
        payment.save()
        return Response({'message': 'Payment rejected successfully'})

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def payment_stats(request):
    """एडमिन डैशबोर्ड के लिए स्टेटिस्टिक्स"""
    total_payments = Payment.objects.count()
    paid_payments = Payment.objects.filter(status='paid').count()
    pending_payments = Payment.objects.filter(status='pending').count()
    total_revenue = Payment.objects.filter(status='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0

    return Response({
        'total_payments': total_payments,
        'paid_payments': paid_payments,
        'pending_payments': pending_payments,
        'total_revenue': total_revenue
    })
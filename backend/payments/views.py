from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import PaymentRecord
from .serializers import PaymentRecordSerializer


class PaymentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PaymentRecordViewSet(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = PaymentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'method', 'date']

    def get_queryset(self):
        """Return all payment records for admin, user-specific for regular users"""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PaymentRecord.objects.all()
        return PaymentRecord.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """Create a new payment record with file upload support"""
        print(f"Payment request method: {request.method}")
        print(f"Payment request content type: {request.content_type}")
        print(f"Payment request data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'Not a dict'}")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create payment record
        payment = serializer.save()

        return Response(
            PaymentRecordSerializer(payment, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get payment history for current user"""
        queryset = self.get_queryset().order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from django.db import transaction
from .models import Seat, SeatBooking
from .serializers import SeatSerializer, SeatBookingSerializer, SeatBookingCreateSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]  # Allow anyone to view seats
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Support file uploads

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """Book a specific seat"""
        seat = self.get_object()

        if seat.status != 'available':
            return Response(
                {'error': 'Seat is not available for booking'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SeatBookingCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                # Create booking
                booking = serializer.save()

                # Update seat status to booked
                seat.status = 'booked'
                seat.save()

                return Response(
                    SeatBookingSerializer(booking).data,
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeatBookingViewSet(viewsets.ModelViewSet):
    queryset = SeatBooking.objects.all()
    serializer_class = SeatBookingSerializer
    permission_classes = [AllowAny]  # Temporarily allow anyone for testing
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Support file uploads

    def get_queryset(self):
        """Return bookings for the current user, or all bookings for anonymous users"""
        if self.request.user.is_authenticated:
            return SeatBooking.objects.filter(user=self.request.user)
        else:
            # For anonymous users, return all bookings (for testing)
            # In production, you might want to return empty queryset or require authentication
            return SeatBooking.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return SeatBookingCreateSerializer
        return SeatBookingSerializer

    def create(self, request, *args, **kwargs):
        """Create a new booking with support for file uploads"""
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'Not a dict'}")

        # Use the serializer directly with request.data - it will handle FormData automatically
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if seat is available
        seat_id = serializer.validated_data['seat'].id
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return Response(
                {'error': 'Seat not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if seat.status != 'available':
            return Response(
                {'error': 'Seat is not available for booking'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for booking conflicts
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        conflicting_bookings = SeatBooking.objects.filter(
            seat=seat,
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if conflicting_bookings.exists():
            return Response(
                {'error': 'Seat is already booked for this time slot'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Create booking
            booking = serializer.save()

            # Update seat status to booked
            seat.status = 'booked'
            seat.save()

            return Response(
                self.get_serializer(booking).data,
                status=status.HTTP_201_CREATED
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()

        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cannot cancel this booking'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Update booking status
            booking.status = 'cancelled'
            booking.save()

            # Check if seat has any other active bookings
            active_bookings = SeatBooking.objects.filter(
                seat=booking.seat,
                status__in=['pending', 'confirmed']
            ).exclude(id=booking.id)

            if not active_bookings.exists():
                # Make seat available again
                booking.seat.status = 'available'
                booking.seat.save()

            return Response({'message': 'Booking cancelled successfully'})

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get booking history for current user"""
        queryset = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
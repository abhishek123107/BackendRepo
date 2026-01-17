from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from django.db.models import Q
from .models import Room, Seat, SeatBooking
from .serializers import RoomSerializer, SeatSerializer, SeatBookingSerializer, SeatBookingCreateSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for library rooms"""

    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class SeatViewSet(viewsets.ModelViewSet):
    """ViewSet for seats"""

    queryset = Seat.objects.filter(is_active=True).select_related('room')
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]  # Allow anyone to view seats

    def get_permissions(self):
        # Allow anyone to view (list, retrieve) seats
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # For other actions (create, update, destroy), require admin
        return [IsAdminUser()]

    def get_queryset(self):
        # Use select_related to prefetch room to avoid N+1 queries and ensure room is loaded
        queryset = Seat.objects.filter(is_active=True).select_related('room')
        room_id = self.request.query_params.get('room', None)
        status_filter = self.request.query_params.get('status', None)

        if room_id:
            queryset = queryset.filter(room_id=room_id)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset


class SeatBookingViewSet(viewsets.ModelViewSet):
    """ViewSet for seat bookings"""

    queryset = SeatBooking.objects.all()
    serializer_class = SeatBookingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Support file uploads

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SeatBooking.objects.all()
        return SeatBooking.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return SeatBookingCreateSerializer
        return SeatBookingSerializer

    def create(self, request, *args, **kwargs):
        """Override create to add logging and handle datetime parsing"""
        # #region agent log
        import json
        import os
        log_file = None
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            log_dir = os.path.join(base_dir, '.cursor')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'debug.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"location": "views.py:73", "message": "SeatBookingViewSet.create called", "data": {"request_data_keys": list(request.data.keys()) if hasattr(request.data, 'keys') else None, "start_time_raw": str(request.data.get('start_time')) if request.data.get('start_time') else None, "end_time_raw": str(request.data.get('end_time')) if request.data.get('end_time') else None}, "timestamp": int(timezone.now().timestamp() * 1000), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "K"}) + "\n")
        except Exception:
            pass
        # #endregion
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_seats(request):
    """Get available seats for booking"""
    date_str = request.query_params.get('date')
    start_time_str = request.query_params.get('start_time')
    end_time_str = request.query_params.get('end_time')
    room_id = request.query_params.get('room')

    if not all([date_str, start_time_str, end_time_str]):
        return Response(
            {'error': 'date, start_time, and end_time are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Parse date and time
        from datetime import datetime
        start_datetime = datetime.fromisoformat(f"{date_str}T{start_time_str}")
        end_datetime = datetime.fromisoformat(f"{date_str}T{end_time_str}")

        # Convert to timezone-aware
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)

        # Get available seats
        seats = Seat.objects.filter(is_active=True, status='available')

        if room_id:
            seats = seats.filter(room_id=room_id)

        available_seats = []
        for seat in seats:
            if seat.is_available_for_booking(start_datetime, end_datetime):
                available_seats.append(seat)

        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)

    except ValueError as e:
        return Response(
            {'error': f'Invalid date/time format: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    """Get current user's bookings"""
    user = request.user
    bookings = SeatBooking.objects.filter(user=user).order_by('-created_at')

    # Filter by status if provided
    status_filter = request.query_params.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    serializer = SeatBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    try:
        booking = SeatBooking.objects.get(id=booking_id, user=request.user)

        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cannot cancel this booking'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.cancel()
        return Response({'status': 'Booking cancelled successfully'})

    except SeatBooking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request, booking_id):
    """Check in to a booking"""
    try:
        booking = SeatBooking.objects.get(id=booking_id, user=request.user)
        booking.check_in()
        return Response({'status': 'Checked in successfully'})
    except SeatBooking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request, booking_id):
    """Check out from a booking"""
    try:
        booking = SeatBooking.objects.get(id=booking_id, user=request.user)
        booking.check_out()
        return Response({'status': 'Checked out successfully'})
    except SeatBooking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

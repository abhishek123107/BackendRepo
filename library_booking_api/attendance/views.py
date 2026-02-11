from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import AttendanceSession, AttendanceRecord
from .serializers import AttendanceSessionSerializer, AttendanceRecordSerializer
from .scanner import qr_scanner


class AttendanceSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for attendance sessions"""

    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AttendanceSession.objects.all()
        return AttendanceSession.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for attendance records"""

    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AttendanceRecord.objects.all()
        return AttendanceRecord.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_qr_checkin(request, token):
    """QR code based attendance check-in"""
    try:
        # Process QR scan using scanner
        qr_data = f"attendance:{token}"
        scan_result = qr_scanner.process_attendance_scan(
            qr_data=qr_data,
            user=request.user,
            scan_location=request.data.get('location', 'Unknown'),
            device_info=request.data.get('device_info', {})
        )
        
        if scan_result['success']:
            serializer = AttendanceRecordSerializer(scan_result['attendance_record'])
            return Response({
                'message': scan_result['message'],
                'record': serializer.data,
                'session': scan_result['session'],
                'check_in_time': scan_result['check_in_time'],
                'status': scan_result['status']
            })
        else:
            return Response(
                {'error': scan_result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Check-in error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_qr_from_image(request):
    """Scan QR code from uploaded image"""
    try:
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        scan_result = qr_scanner.scan_qr_from_image(image_file)
        
        if scan_result['success']:
            return Response({
                'success': True,
                'qr_data': scan_result['qr_data'],
                'confidence': scan_result['confidence'],
                'position': scan_result['position'],
                'quality': scan_result['quality']
            })
        else:
            return Response({
                'success': False,
                'error': scan_result['error'],
                'confidence': scan_result['confidence']
            })
            
    except Exception as e:
        return Response(
            {'error': f'Scanning error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_attendance_scan(request):
    """Process QR code scan for attendance"""
    try:
        qr_data = request.data.get('qr_data')
        if not qr_data:
            return Response(
                {'error': 'QR data is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scan_result = qr_scanner.process_attendance_scan(
            qr_data=qr_data,
            user=request.user,
            scan_location=request.data.get('location'),
            device_info=request.data.get('device_info')
        )
        
        if scan_result['success']:
            serializer = AttendanceRecordSerializer(scan_result['attendance_record'])
            return Response({
                'success': True,
                'message': scan_result['message'],
                'record': serializer.data,
                'session': scan_result['session'],
                'check_in_time': scan_result['check_in_time'],
                'status': scan_result['status']
            })
        else:
            return Response({
                'success': False,
                'error': scan_result['error']
            })
            
    except Exception as e:
        return Response(
            {'error': f'Processing error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_attendance(request):
    """Get current user's attendance records"""
    user = request.user
    records = AttendanceRecord.objects.filter(user=user).order_by('-check_in_time')

    # Filter by date range if provided
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if start_date:
        records = records.filter(check_in_time__date__gte=start_date)
    if end_date:
        records = records.filter(check_in_time__date__lte=end_date)

    serializer = AttendanceRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def session_stats(request, session_id):
    """Get attendance statistics for a session"""
    session = get_object_or_404(AttendanceSession, id=session_id)

    total_records = AttendanceRecord.objects.filter(session=session).count()
    qr_checkins = AttendanceRecord.objects.filter(session=session, method='qr').count()
    admin_checkins = AttendanceRecord.objects.filter(session=session, method='admin').count()

    # Calculate attendance rate if max_participants is set
    attendance_rate = None
    if session.max_participants:
        attendance_rate = (total_records / session.max_participants) * 100

    return Response({
        'session_id': session.id,
        'session_title': session.title,
        'total_attendance': total_records,
        'qr_checkins': qr_checkins,
        'admin_checkins': admin_checkins,
        'attendance_rate': attendance_rate,
        'max_participants': session.max_participants
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_checkin(request, session_id):
    """Admin manual check-in for a user"""
    session = get_object_or_404(AttendanceSession, id=session_id)
    user_id = request.data.get('user_id')

    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    from accounts.models import User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if already checked in
    existing_record = AttendanceRecord.objects.filter(
        session=session,
        user=user
    ).first()

    if existing_record:
        return Response(
            {'error': 'User already checked in'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create attendance record
    record = AttendanceRecord.objects.create(
        session=session,
        user=user,
        check_in_time=timezone.now(),
        method='admin',
        marked_by=request.user
    )

    serializer = AttendanceRecordSerializer(record)
    return Response({
        'message': 'Check-in recorded successfully',
        'record': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def attendance_report(request):
    """Generate attendance report"""
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    user_id = request.query_params.get('user_id')

    records = AttendanceRecord.objects.all()

    if start_date:
        records = records.filter(check_in_time__date__gte=start_date)
    if end_date:
        records = records.filter(check_in_time__date__lte=end_date)
    if user_id:
        records = records.filter(user_id=user_id)

    # Group by user and calculate stats
    from django.db.models import Count
    user_stats = records.values('user__email', 'user__first_name', 'user__last_name').annotate(
        total_sessions=Count('id')
    ).order_by('-total_sessions')

    return Response({
        'total_records': records.count(),
        'user_statistics': list(user_stats),
        'date_range': {
            'start': start_date,
            'end': end_date
        }
    })

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import datetime, timedelta
import logging
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return UserRegistrationSerializer
        if self.action == 'login':
            return LoginSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], parser_classes=[JSONParser, FormParser, MultiPartParser])
    def login(self, request):
        """User login with email/phone and password"""
        # Check if request body is present
        if not request.data:
            logger.warning('Login attempt with empty request body')
            return Response({'detail': 'Request body is empty or not valid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        # Debug logging to see what data is received
        logger.info(f'Login request data keys: {list(request.data.keys())}')
        logger.info(f'Login request data: {request.data}')

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f'Login validation failed: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data.get('user')
        if not user:
            logger.warning('Login successful validation but no user in data')
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        logger.info(f'User {user.username} logged in successfully')
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], parser_classes=[JSONParser, FormParser, MultiPartParser])
    def register(self, request):
        """User registration"""
        if not request.data:
            logger.warning('Registration attempt with empty request body')
            return Response({'detail': 'Request body is empty or not valid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f'New user registered: {user.username} ({user.email})')
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f'Error creating user: {str(e)}')
                return Response(
                    {'detail': f'Error creating user: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        logger.warning(f'Registration validation failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get all users (for admin panel)"""
        # Only allow staff users to access this endpoint
        if not request.user.is_staff:
            return Response(
                {'detail': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """Verify JWT token"""
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'valid': False, 'detail': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        AccessToken(token)
        return Response({'valid': True})
    except (InvalidToken, TokenError) as e:
        return Response({'valid': False, 'detail': str(e)})


# Student Dashboard APIs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    """Get complete student dashboard data"""
    user = request.user
    
    # Get student profile
    profile_data = UserSerializer(user).data
    
    # Get student statistics
    stats_data = get_student_stats(user)
    
    # Get recent activities
    activities_data = get_recent_activities(user, limit=5)
    
    # Get notifications
    notifications_data = get_student_notifications(user)
    
    return Response({
        'profile': profile_data,
        'stats': stats_data,
        'recent_activities': activities_data,
        'notifications': notifications_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    """Get student profile information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def student_profile_update(request):
    """Update student profile information"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_stats(request):
    """Get student statistics"""
    stats = get_student_stats(request.user)
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_activities(request):
    """Get student recent activities"""
    limit = int(request.GET.get('limit', 10))
    activities = get_recent_activities(request.user, limit)
    return Response(activities)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_bookings(request):
    """Get student booking history"""
    # This would integrate with seats app
    # For now, return mock data
    status_filter = request.GET.get('status')
    
    bookings = [
        {
            'id': 1,
            'seat_number': 'A-15',
            'date': '2026-01-18',
            'start_time': '09:00',
            'end_time': '12:00',
            'status': 'active',
            'created_at': '2026-01-18T08:30:00Z'
        },
        {
            'id': 2,
            'seat_number': 'B-08',
            'date': '2026-01-17',
            'start_time': '14:00',
            'end_time': '17:00',
            'status': 'completed',
            'created_at': '2026-01-17T13:30:00Z'
        }
    ]
    
    if status_filter:
        bookings = [b for b in bookings if b['status'] == status_filter]
    
    return Response(bookings)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_attendance(request):
    """Get student attendance records"""
    # This would integrate with attendance app
    # For now, return mock data
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    attendance = [
        {
            'id': 1,
            'date': '2026-01-18',
            'check_in_time': '09:15',
            'check_out_time': '12:30',
            'status': 'present',
            'session_title': 'Daily Attendance - 2026-01-18'
        },
        {
            'id': 2,
            'date': '2026-01-17',
            'check_in_time': '09:30',
            'check_out_time': None,
            'status': 'present',
            'session_title': 'Daily Attendance - 2026-01-17'
        }
    ]
    
    return Response(attendance)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_payments(request):
    """Get student payment history"""
    # This would integrate with payments app
    # For now, return mock data
    payments = [
        {
            'id': 1,
            'amount': 1000.00,
            'payment_type': 'membership',
            'status': 'completed',
            'created_at': '2026-01-15T10:00:00Z',
            'verified_at': '2026-01-15T11:30:00Z'
        },
        {
            'id': 2,
            'amount': 500.00,
            'payment_type': 'fine',
            'status': 'pending',
            'created_at': '2026-01-18T14:00:00Z',
            'verified_at': None
        }
    ]
    
    return Response(payments)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    """Upload student avatar"""
    if 'avatar' not in request.FILES:
        return Response(
            {'error': 'No avatar file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    avatar_file = request.FILES['avatar']
    user = request.user
    
    # For now, just return a mock URL
    # In production, you would upload to cloud storage
    avatar_url = f"https://example.com/avatars/{user.id}_{avatar_file.name}"
    
    user.avatar = avatar_url
    user.save()
    
    return Response({'avatar': avatar_url})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change student password"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {'error': 'Both old and new passwords are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    
    if not user.check_password(old_password):
        return Response(
            {'error': 'Current password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password changed successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def membership_details(request):
    """Get student membership details"""
    user = request.user
    
    membership_info = {
        'type': user.membership_type,
        'status': 'Active' if user.is_active else 'Inactive',
        'expiry_date': user.membership_expiry,
        'days_until_expiry': None,
        'benefits': get_membership_benefits(user.membership_type)
    }
    
    if user.membership_expiry:
        expiry_date = user.membership_expiry.date()
        today = timezone.now().date()
        membership_info['days_until_expiry'] = (expiry_date - today).days
    
    return Response(membership_info)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_membership(request):
    """Upgrade student membership"""
    membership_type = request.data.get('membership_type')
    
    if membership_type not in ['basic', 'premium', 'vip']:
        return Response(
            {'error': 'Invalid membership type'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    
    # For demo purposes, just update the membership type
    # In production, this would involve payment processing
    user.membership_type = membership_type
    
    # Set expiry date (30 days from now)
    user.membership_expiry = timezone.now() + timedelta(days=30)
    user.save()
    
    return Response({
        'message': f'Membership upgraded to {membership_type}',
        'membership_type': membership_type,
        'expiry_date': user.membership_expiry
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_notifications(request):
    """Get student notifications"""
    # Mock notifications data
    notifications = [
        {
            'id': 1,
            'title': 'Library Closure Notice',
            'message': 'Library will be closed on Sunday for maintenance.',
            'type': 'info',
            'read': False,
            'created_at': '2026-01-18T10:00:00Z'
        },
        {
            'id': 2,
            'title': 'Payment Reminder',
            'message': 'Your membership fee is due for renewal.',
            'type': 'warning',
            'read': False,
            'created_at': '2026-01-17T15:30:00Z'
        }
    ]
    
    return Response(notifications)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    # Mock implementation
    return Response({'message': 'Notification marked as read'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard_position(request):
    """Get student's position in leaderboard"""
    # Mock implementation
    return Response({
        'position': 15,
        'total_students': 100,
        'score': 850,
        'rank_change': '+3'
    })


# Helper functions
def get_student_stats(user):
    """Calculate student statistics"""
    # Mock calculations - in production, these would be real database queries
    return {
        'total_bookings': 5,
        'active_bookings': 1,
        'completed_bookings': 4,
        'cancelled_bookings': 0,
        'total_attendance_days': 12,
        'attendance_percentage': 85.5,
        'total_payments': 3,
        'pending_payments': 1,
        'membership_status': 'Active',
        'days_until_expiry': 15
    }


def get_recent_activities(user, limit=10):
    """Get student's recent activities"""
    # Mock activities - in production, these would be real database records
    activities = [
        {
            'id': 1,
            'type': 'booking',
            'title': 'Seat Booked',
            'description': 'Seat A-15 booked for Study Room',
            'timestamp': '2026-01-18T08:30:00Z',
            'status': 'completed'
        },
        {
            'id': 2,
            'type': 'attendance',
            'title': 'Attendance Marked',
            'description': 'Daily attendance marked successfully',
            'timestamp': '2026-01-17T09:15:00Z',
            'status': 'completed'
        },
        {
            'id': 3,
            'type': 'payment',
            'title': 'Payment Submitted',
            'description': 'Membership fee payment submitted',
            'timestamp': '2026-01-15T10:00:00Z',
            'status': 'pending'
        }
    ]
    
    return activities[:limit]


def get_student_notifications(user):
    """Get student notifications"""
    # Mock notifications
    return [
        {
            'id': 1,
            'title': 'Library Closure Notice',
            'message': 'Library will be closed on Sunday for maintenance.',
            'type': 'info',
            'read': False,
            'created_at': '2026-01-18T10:00:00Z'
        }
    ]


def get_membership_benefits(membership_type):
    """Get membership benefits based on type"""
    benefits = {
        'basic': [
            'Seat booking (up to 2 hours)',
            'Basic library access',
            'Attendance tracking'
        ],
        'premium': [
            'Seat booking (up to 4 hours)',
            'Priority booking',
            'Extended library access',
            'Attendance tracking',
            'Discount on events'
        ],
        'vip': [
            'Unlimited seat booking',
            'VIP room access',
            '24/7 library access',
            'Personalized assistance',
            'Free event access',
            'Priority support'
        ]
    }
    
    return benefits.get(membership_type, benefits['basic'])


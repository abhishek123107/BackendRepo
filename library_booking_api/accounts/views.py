from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate
from django.utils import timezone
import logging
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login', 'register', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return UserRegistrationSerializer
        if self.action == 'login':
            return LoginSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action == 'list':
            # For list action, return all users for admin panel
            return User.objects.all()
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


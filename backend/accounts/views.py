from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer


class APIRootView(APIView):
    """API Root View for Accounts"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'Library Seat Booking - Accounts API',
            'version': '1.0.0',
            'endpoints': {
                'login': 'login/',
                'register': 'register/',
                'profile': 'profile/',
                'token_refresh': 'token/refresh/'
            }
        })


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')

        if not email_or_phone or not password:
            return Response(
                {'error': 'Email/Phone and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to authenticate with email first, then username
        user = None
        if '@' in email_or_phone:
            # Email login
            try:
                user_obj = User.objects.get(email=email_or_phone)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            # Username login
            user = authenticate(username=email_or_phone, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user': UserSerializer(user).data
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

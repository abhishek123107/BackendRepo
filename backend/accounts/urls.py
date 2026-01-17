from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # API root endpoint
    path('', views.APIRootView.as_view(), name='api_root'),
    
    # JWT token endpoints
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom auth endpoints
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
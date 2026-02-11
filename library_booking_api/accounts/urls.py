from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'}), name='users-list'),
    path('login/', views.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', views.UserViewSet.as_view({'post': 'register'}), name='register'),
    path('profile/', views.UserViewSet.as_view({'get': 'profile', 'put': 'update_profile', 'patch': 'update_profile'}), name='profile'),
    path('token/verify/', views.verify_token, name='token-verify'),
]
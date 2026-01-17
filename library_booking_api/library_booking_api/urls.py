from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import UserViewSet
from seats.views import RoomViewSet, SeatViewSet, SeatBookingViewSet
from attendance.views import AttendanceSessionViewSet, AttendanceRecordViewSet
from payments.views import MembershipPlanViewSet, PaymentViewSet

# Create a single router to avoid converter conflicts
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rooms', RoomViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', SeatBookingViewSet)
router.register(r'sessions', AttendanceSessionViewSet)
router.register(r'records', AttendanceRecordViewSet)
router.register(r'plans', MembershipPlanViewSet, basename='membership-plans')
router.register(r'payments', PaymentViewSet, basename='payment-records')

# होम व्यू: यह चेक करने के लिए कि API सही से काम कर रही है
def home(request):
    """API Home endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Library Seat Booking API is Running',
        'endpoints': {
            'auth_token': '/api/auth/token/',
            'accounts': '/api/accounts/',
            'seats': '/api/seats/',
            'attendance': '/api/attendance/',
            'payments': '/api/payments/',
            'admin_panel': '/admin/',
        }
    })

urlpatterns = [
    # Root URL (404 एरर से बचने के लिए)
    path('', home, name='home'),
    
    # Admin Panel
    path('admin/', admin.site.urls),

    # JWT Authentication (Login & Refresh)
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Router (all endpoints in one place to avoid converter conflicts)
    path('api/', include(router.urls)),
    
    # Additional custom endpoints from individual apps
    path('api/accounts/', include('accounts.urls')),
    path('api/seats/', include('seats.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# Development के दौरान Media (Screenshots) और Static फाइल्स सर्व करने के लिए
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
"""
URL configuration for library_seat_booking project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from attendance.views import AttendanceRecordViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('seats.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/records/', AttendanceRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='records'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
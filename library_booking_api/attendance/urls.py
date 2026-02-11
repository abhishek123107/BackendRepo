from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('sessions/', views.AttendanceSessionViewSet.as_view({'get': 'list'}), name='attendance-sessions'),
    path('qr-checkin/<str:token>/', views.attendance_qr_checkin, name='attendance-qr-checkin'),
    path('scan-qr-image/', views.scan_qr_from_image, name='scan-qr-image'),
    path('process-scan/', views.process_attendance_scan, name='process-attendance-scan'),
    path('my-attendance/', views.my_attendance, name='my-attendance'),
    path('session-stats/<int:session_id>/', views.session_stats, name='session-stats'),
    path('admin-checkin/<int:session_id>/', views.admin_checkin, name='admin-checkin'),
    path('report/', views.attendance_report, name='attendance-report'),
]
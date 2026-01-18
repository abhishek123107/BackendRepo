from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('records/', views.AttendanceRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='attendance-records'),
    path('records/<int:pk>/', views.AttendanceRecordViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='attendance-record-detail'),
    path('sessions/', views.AttendanceSessionViewSet.as_view({'get': 'list', 'post': 'create'}), name='attendance-sessions'),
    path('sessions/<int:pk>/', views.AttendanceSessionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='attendance-session-detail'),
    path('qr-checkin/<str:token>/', views.attendance_qr_checkin, name='attendance-qr-checkin'),
    path('my-attendance/', views.my_attendance, name='my-attendance'),
    path('session-stats/<int:session_id>/', views.session_stats, name='session-stats'),
    path('admin-checkin/<int:session_id>/', views.admin_checkin, name='admin-checkin'),
    path('generate-qr/', views.generate_qr_code, name='generate-qr'),
    path('report/', views.attendance_report, name='attendance-report'),
]
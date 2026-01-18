from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('qr-checkin/<str:token>/', views.attendance_qr_checkin, name='attendance-qr-checkin'),
    path('my-attendance/', views.my_attendance, name='my-attendance'),
    path('session-stats/<int:session_id>/', views.session_stats, name='session-stats'),
    path('admin-checkin/<int:session_id>/', views.admin_checkin, name='admin-checkin'),
    path('report/', views.attendance_report, name='attendance-report'),
]
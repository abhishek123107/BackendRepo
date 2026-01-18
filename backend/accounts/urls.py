from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('login/', views.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', views.UserViewSet.as_view({'post': 'register'}), name='register'),
    path('profile/', views.UserViewSet.as_view({'get': 'profile', 'put': 'update_profile', 'patch': 'update_profile'}), name='profile'),
    path('users/', views.UserViewSet.as_view({'get': 'users'}), name='users'),
    path('token/verify/', views.verify_token, name='token-verify'),
    
    # Student Dashboard APIs
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('student/profile/', views.student_profile, name='student-profile'),
    path('student/profile/update/', views.student_profile_update, name='student-profile-update'),
    path('student/stats/', views.student_stats, name='student-stats'),
    path('student/activities/', views.student_activities, name='student-activities'),
    path('student/bookings/', views.student_bookings, name='student-bookings'),
    path('student/attendance/', views.student_attendance, name='student-attendance'),
    path('student/payments/', views.student_payments, name='student-payments'),
    path('student/upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('student/change-password/', views.change_password, name='change-password'),
    path('student/membership/', views.membership_details, name='membership-details'),
    path('student/upgrade-membership/', views.upgrade_membership, name='upgrade-membership'),
    path('student/notifications/', views.student_notifications, name='student-notifications'),
    path('student/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('student/leaderboard/', views.leaderboard_position, name='leaderboard-position'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('my-notifications/', views.UserNotificationViewSet.as_view({'get': 'my_notifications'}), name='my-notifications'),
    path('user-notifications/<int:pk>/mark-as-read/', views.UserNotificationViewSet.as_view({'post': 'mark_as_read'}), name='mark-notification-read'),
]

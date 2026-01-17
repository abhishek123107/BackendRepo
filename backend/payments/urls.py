from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.PaymentRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-records'),
    path('records/history/', views.PaymentRecordViewSet.as_view({'get': 'history'}), name='payment-history'),
    path('records/<int:pk>/', views.PaymentRecordViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='payment-detail'),
    path('records/<int:pk>/approve/', views.PaymentRecordViewSet.as_view({'post': 'approve'}), name='payment-approve'),
    path('records/<int:pk>/reject/', views.PaymentRecordViewSet.as_view({'post': 'reject'}), name='payment-reject'),
]

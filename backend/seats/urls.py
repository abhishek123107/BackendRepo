from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeatViewSet, SeatBookingViewSet

router = DefaultRouter()
router.register(r'seats', SeatViewSet)
router.register(r'bookings', SeatBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
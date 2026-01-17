from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('available-seats/', views.available_seats, name='available-seats'),
    path('my-bookings/', views.my_bookings, name='my-bookings'),
]
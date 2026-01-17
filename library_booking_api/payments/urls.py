from django.urls import path
from . import views

# Only custom endpoints, ViewSets are handled by main router
urlpatterns = [
    path('stats/', views.payment_stats, name='payment-stats'),
]
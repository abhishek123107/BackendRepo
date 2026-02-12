from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def root_view(request):
    """
    Root URL view that returns server status
    """
    response_data = {
        "message": "Backend Server is Running Successfully",
        "status": "active",
        "service": "Library Seat Booking API",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "accounts": "/api/accounts/",
            "auth": "/api/auth/",
            "payments": "/api/payments/",
            "attendance": "/api/attendance/",
            "notifications": "/api/notifications/",
            "records": "/api/records/"
        },
        "documentation": "/api/docs/"
    }
    
    return JsonResponse(response_data, status=200)

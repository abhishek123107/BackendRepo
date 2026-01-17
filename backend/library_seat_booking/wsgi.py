"""
WSGI config for library_seat_booking project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_seat_booking.settings')

application = get_wsgi_application()
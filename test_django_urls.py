#!/usr/bin/env python3
import os
import sys
import django

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_seat_booking.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

def print_url_patterns():
    """Print all URL patterns"""
    resolver = get_resolver()
    
    def print_patterns(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                # This is an include
                print_patterns(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                print(f"{prefix + str(pattern.pattern)} -> {pattern.callback}")

    print("=== URL Patterns ===")
    print_patterns(resolver.url_patterns)

if __name__ == "__main__":
    print_url_patterns()

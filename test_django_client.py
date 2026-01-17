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

from django.test import Client
from seats.models import Seat, SeatBooking
import json

def test_with_django_client():
    """Test API endpoints using Django's test client"""
    client = Client()
    
    print("=== Testing with Django Test Client ===")
    
    # Test seats endpoint
    print("\n1. Testing /api/seats/")
    response = client.get('/api/seats/')
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Response Type: {type(data)}")
        if isinstance(data, list):
            print(f"Response is a list with {len(data)} items")
            if data:
                print(f"First item keys: {list(data[0].keys())}")
                print(f"First item: {json.dumps(data[0], indent=2)}")
        else:
            print(f"Response data: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Error: {response.content.decode()}")
    
    # Test bookings endpoint
    print("\n2. Testing /api/bookings/")
    response = client.get('/api/bookings/')
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Response Type: {type(data)}")
        if isinstance(data, list):
            print(f"Response is a list with {len(data)} items")
            if data:
                print(f"First item keys: {list(data[0].keys())}")
        else:
            print(f"Response data: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Error: {response.content.decode()}")

    # Check database state
    print(f"\n3. Database State:")
    print(f"Seats count: {Seat.objects.count()}")
    print(f"Bookings count: {SeatBooking.objects.count()}")
    
    # Show sample seat
    first_seat = Seat.objects.first()
    if first_seat:
        print(f"First seat: {first_seat}")
        print(f"First seat data: id={first_seat.id}, number={first_seat.number}, status={first_seat.status}")

if __name__ == "__main__":
    test_with_django_client()

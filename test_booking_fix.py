#!/usr/bin/env python
"""
Test booking creation with payment
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api"

def test_booking_creation():
    print("🚀 Testing Booking Creation with Payment...")
    
    # Login as user
    login_data = {
        "email_or_phone": "testapi",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    token_data = response.json()
    access_token = token_data.get('access')
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print("✅ Login successful")
    
    # Get available seats
    response = requests.get(f"{BASE_URL}/seats/", headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to get seats: {response.text}")
        return False
    
    seats_data = response.json()
    # Handle paginated response
    seats = seats_data if isinstance(seats_data, list) else seats_data.get('results', [])
    
    if not seats:
        print("❌ No seats available")
        return False
    
    # Use first available seat
    seat_id = seats[0]['id']
    print(f"✅ Using seat {seat_id}")
    
    # Create booking with payment screenshot
    booking_data = {
        "seat": seat_id,
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=3)).isoformat(),
        "purpose": "Test booking with payment"
    }
    
    print("📝 Creating booking with payment...")
    response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        booking = response.json()
        print("✅ Booking created successfully!")
        print(f"  Booking ID: {booking.get('id')}")
        print(f"  Seat: {booking.get('seat')}")
        print(f"  Payment: {booking.get('payment')}")
        return True
    else:
        print(f"❌ Booking creation failed: {response.text}")
        return False

if __name__ == "__main__":
    test_booking_creation()

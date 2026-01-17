#!/usr/bin/env python
"""
Test both booking scenarios
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api"

def test_booking_scenarios():
    print("🚀 Testing Booking Creation Scenarios...")
    
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
    seats_data = response.json()
    seats = seats_data if isinstance(seats_data, list) else seats_data.get('results', [])
    
    if not seats:
        print("❌ No seats available")
        return False
    
    seat_id = seats[0]['id']
    print(f"✅ Using seat {seat_id}")
    
    # Test 1: Simple booking without payment
    print("\n1. Testing simple booking without payment:")
    booking_data = {
        "seat": seat_id,
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=3)).isoformat(),
        "purpose": "Test booking without payment"
    }
    
    response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        booking = response.json()
        print("✅ Simple booking created successfully!")
        print(f"  Booking ID: {booking.get('id')}")
        print(f"  Payment: {booking.get('payment')}")
    else:
        print(f"❌ Simple booking failed: {response.text}")
        return False
    
    # Test 2: Booking with existing payment ID
    print("\n2. Testing booking with payment ID:")
    # First create a payment
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    payment_data = {
        "description": "Test Payment for Booking",
        "amount": "100.00",
        "method": "online",
        "date": "2025-01-17",
        "account_holder_name": "Test User",
        "transaction_id": f"BOOK{unique_id}"
    }
    
    response = requests.post(f"{BASE_URL}/payments/", json=payment_data, headers=headers)
    if response.status_code == 201:
        payment = response.json()
        payment_id = payment.get('id')
        print(f"✅ Payment created: ID {payment_id}")
        
        # Now create booking with payment_id
        booking_data = {
            "seat": seat_id,
            "start_time": (datetime.now() + timedelta(hours=4)).isoformat(),
            "end_time": (datetime.now() + timedelta(hours=6)).isoformat(),
            "purpose": "Test booking with payment ID",
            "payment_id": payment_id
        }
        
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            booking = response.json()
            print("✅ Booking with payment ID created successfully!")
            print(f"  Booking ID: {booking.get('id')}")
            print(f"  Payment: {booking.get('payment')}")
            return True
        else:
            print(f"❌ Booking with payment ID failed: {response.text}")
            return False
    else:
        print(f"❌ Payment creation failed: {response.text}")
        return False

if __name__ == "__main__":
    success = test_booking_scenarios()
    print(f"\n🎉 Booking system test: {'PASSED' if success else 'FAILED'}")

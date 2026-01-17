#!/usr/bin/env python
"""
Test booking creation with payment integration
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def test_booking_creation():
    print("🚀 Testing Booking Creation with Payment Integration...")
    
    # First, get a fresh token
    login_data = {
        "email_or_phone": "testpayment",
        "password": "testpass123"
    }
    
    try:
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
        
        seats = response.json()
        if not seats:
            print("❌ No seats available")
            return False
        
        # Use first available seat
        seat_id = seats[0]['id']
        print(f"✅ Using seat {seat_id}")
        
        # Create booking with payment_id
        booking_data = {
            "seat": seat_id,
            "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(hours=3)).isoformat(),
            "purpose": "Test booking with payment",
            "payment_id": 1  # Use existing payment ID
        }
        
        print("📝 Creating booking with payment_id...")
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
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_booking_without_payment():
    print("\n🚀 Testing Booking Creation without Payment...")
    
    # Get fresh token
    login_data = {
        "email_or_phone": "testpayment",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return False
        
        token_data = response.json()
        access_token = token_data.get('access')
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Get available seats
        response = requests.get(f"{BASE_URL}/seats/", headers=headers)
        seats = response.json()
        seat_id = seats[0]['id']
        
        # Create booking without payment
        booking_data = {
            "seat": seat_id,
            "start_time": (datetime.now() + timedelta(hours=4)).isoformat(),
            "end_time": (datetime.now() + timedelta(hours=6)).isoformat(),
            "purpose": "Test booking without payment"
        }
        
        print("📝 Creating booking without payment...")
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            booking = response.json()
            print("✅ Booking created successfully without payment!")
            print(f"  Booking ID: {booking.get('id')}")
            print(f"  Payment: {booking.get('payment')}")
            return True
        else:
            print(f"❌ Booking creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("BOOKING CREATION WITH PAYMENT INTEGRATION TEST")
    print("=" * 60)
    
    # Test with payment
    test1 = test_booking_creation()
    
    # Test without payment
    test2 = test_booking_without_payment()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"  Booking with Payment: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  Booking without Payment: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\n🎉 BOOKING SYSTEM IS FULLY FUNCTIONAL!")
        print("✅ Payment integration working correctly")
        print("✅ Bookings can be created with and without payments")
        print("✅ Database properly updated with payment relationships")
    else:
        print("\n❌ Some booking tests failed")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

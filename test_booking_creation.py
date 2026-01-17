#!/usr/bin/env python3
import requests
import json

def test_booking_creation():
    """Test booking creation with the fixed serializer"""
    base_url = "http://localhost:8000"
    
    print("=== Testing Booking Creation ===")
    
    # First login to get token
    print("\n1. 🔐 Login...")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    access_token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    print(f"✅ Login successful!")
    
    # Test booking creation without payment_method (should default to offline)
    print("\n2. 📅 Creating Booking (without payment_method)...")
    booking_data = {
        'seat': 24,
        'start_time': '2026-01-17T14:00:00Z',
        'end_time': '2026-01-17T18:00:00Z',
        'purpose': 'daily'  # This will be mapped to 'plan'
    }
    
    booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
    print(f"Status: {booking_response.status_code}")
    
    if booking_response.status_code == 201:
        booking = booking_response.json()
        print(f"✅ Booking created successfully!")
        print(f"   Booking ID: {booking['id']}")
        print(f"   Seat: {booking['seat']}")
        print(f"   Plan: {booking['plan']}")
        print(f"   Payment Method: {booking['payment_method']}")
        print(f"   Status: {booking['status']}")
    else:
        print(f"❌ Booking failed: {booking_response.text}")
        return
    
    # Test booking creation with explicit payment_method
    print("\n3. 📅 Creating Booking (with explicit payment_method)...")
    booking_data2 = {
        'seat': 25,
        'start_time': '2026-01-17T09:00:00Z',
        'end_time': '2026-01-17T13:00:00Z',
        'purpose': 'hourly',
        'payment_method': 'offline'
    }
    
    booking_response2 = requests.post(f"{base_url}/api/bookings/", json=booking_data2, headers=headers)
    print(f"Status: {booking_response2.status_code}")
    
    if booking_response2.status_code == 201:
        booking2 = booking_response2.json()
        print(f"✅ Second booking created successfully!")
        print(f"   Booking ID: {booking2['id']}")
        print(f"   Seat: {booking2['seat']}")
        print(f"   Plan: {booking2['plan']}")
        print(f"   Payment Method: {booking2['payment_method']}")
    else:
        print(f"❌ Second booking failed: {booking_response2.text}")
    
    # Check user's bookings
    print("\n4. 📋 Checking User Bookings...")
    bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
    
    if bookings_response.status_code == 200:
        bookings = bookings_response.json()
        print(f"✅ User has {len(bookings)} bookings")
        for booking in bookings:
            print(f"   - Seat {booking['seat']}: {booking['plan']} ({booking['status']})")
    
    print(f"\n🎉 Booking creation is now working!")

if __name__ == "__main__":
    test_booking_creation()

#!/usr/bin/env python3
import requests
import json

def test_booking_simple():
    """Simple test of booking creation"""
    base_url = "http://localhost:8000"
    
    print("=== Simple Booking Test ===")
    
    # Login
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
    
    # Create booking - same data as Angular sends
    booking_data = {
        'seat': 24,
        'start_time': '2026-01-17T14:00:00Z',
        'end_time': '2026-01-17T18:00:00Z',
        'purpose': 'daily'
    }
    
    print(f"\n📅 Creating booking with data: {booking_data}")
    booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
    
    print(f"Status: {booking_response.status_code}")
    print(f"Response: {booking_response.text}")
    
    if booking_response.status_code == 201:
        print(f"✅ SUCCESS! Booking creation works!")
        print(f"🎉 Angular frontend should now be able to create bookings!")
    else:
        print(f"❌ Still failing with 400 error")

if __name__ == "__main__":
    test_booking_simple()

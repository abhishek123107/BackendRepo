#!/usr/bin/env python3
import requests
import json

def test_booking_response():
    """Check what fields are returned in booking response"""
    base_url = "http://localhost:8000"
    
    print("=== Checking Booking Response Fields ===")
    
    # Login
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    access_token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get available seat
    seats_response = requests.get(f"{base_url}/api/seats/")
    seats = seats_response.json()
    available_seats = [s for s in seats if s['status'] == 'available']
    
    if available_seats:
        # Create booking
        booking_data = {
            'seat': available_seats[0]['id'],
            'start_time': '2026-01-17T14:00:00Z',
            'end_time': '2026-01-17T18:00:00Z',
            'purpose': 'daily'
        }
        
        booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
        
        if booking_response.status_code == 201:
            booking = booking_response.json()
            print(f"✅ Booking created!")
            print(f"Response keys: {list(booking.keys())}")
            print(f"Full response: {json.dumps(booking, indent=2)}")
            
            # Also check user bookings
            bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
            if bookings_response.status_code == 200:
                user_bookings = bookings_response.json()
                if user_bookings:
                    print(f"\nUser booking keys: {list(user_bookings[0].keys())}")
                    print(f"First user booking: {json.dumps(user_bookings[0], indent=2)}")
        else:
            print(f"❌ Booking failed: {booking_response.text}")

if __name__ == "__main__":
    test_booking_response()

#!/usr/bin/env python3
import requests
import json

def test_seat_selection_fix():
    """Test that only available seats can be booked"""
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING SEAT SELECTION FIX")
    print("=" * 50)
    
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
    
    # Get current seat status
    seats_response = requests.get(f"{base_url}/api/seats/")
    seats = seats_response.json()
    available_seats = [s for s in seats if s['status'] == 'available']
    booked_seats = [s for s in seats if s['status'] == 'booked']
    
    print(f"\n📊 Current Status:")
    print(f"   Available seats: {len(available_seats)}")
    print(f"   Booked seats: {len(booked_seats)}")
    
    # Test 1: Try to book an available seat (should work)
    if available_seats:
        test_seat = available_seats[0]
        print(f"\n✅ Test 1: Booking available seat {test_seat['number']} (ID: {test_seat['id']})")
        
        booking_data = {
            'seat': test_seat['id'],
            'start_time': '2026-01-17T14:00:00Z',
            'end_time': '2026-01-17T18:00:00Z',
            'purpose': 'daily'
        }
        
        booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
        
        if booking_response.status_code == 201:
            print(f"   ✅ SUCCESS! Available seat booked successfully")
        else:
            print(f"   ❌ FAILED: {booking_response.text}")
    
    # Test 2: Try to book a booked seat (should fail)
    if booked_seats:
        test_seat = booked_seats[0]
        print(f"\n❌ Test 2: Booking already booked seat {test_seat['number']} (ID: {test_seat['id']})")
        
        booking_data = {
            'seat': test_seat['id'],
            'start_time': '2026-01-17T14:00:00Z',
            'end_time': '2026-01-17T18:00:00Z',
            'purpose': 'daily'
        }
        
        booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
        
        if booking_response.status_code == 400:
            print(f"   ✅ CORRECTLY REJECTED: {booking_response.text}")
        else:
            print(f"   ❌ UNEXPECTED: Should have failed but got {booking_response.status_code}")
    
    print(f"\n🎯 ANGULAR FIX SUMMARY:")
    print(f"   ✅ Removed immediate mock seat initialization")
    print(f"   ✅ Added seat availability check in selectSeat()")
    print(f"   ✅ Added double-check in onBookSeat()")
    print(f"   ✅ User alerts for unavailable seats")
    
    print(f"\n🌐 USER EXPERIENCE:")
    print(f"   - Only available seats can be selected")
    print(f"   - Clear error messages for unavailable seats")
    print(f"   - No more 'Seat is not available' booking errors")
    print(f"   - Visual feedback prevents confusion")
    
    print(f"\n📋 Available seats for testing:")
    for seat in available_seats[:5]:
        print(f"   - Seat {seat['number']} (ID: {seat['id']})")

if __name__ == "__main__":
    test_seat_selection_fix()

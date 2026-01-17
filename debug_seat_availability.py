#!/usr/bin/env python3
import requests
import json

def debug_seat_availability():
    """Debug seat availability issues"""
    base_url = "http://localhost:8000"
    
    print("🔍 DEBUGGING SEAT AVAILABILITY")
    print("=" * 50)
    
    # Get current seat status
    print("\n1️⃣ Current Seat Status:")
    seats_response = requests.get(f"{base_url}/api/seats/")
    
    if seats_response.status_code == 200:
        seats = seats_response.json()
        available_seats = [s for s in seats if s['status'] == 'available']
        booked_seats = [s for s in seats if s['status'] == 'booked']
        
        print(f"   Total seats: {len(seats)}")
        print(f"   Available seats: {len(available_seats)}")
        print(f"   Booked seats: {len(booked_seats)}")
        
        print(f"\n   Available seat numbers: {[s['number'] for s in available_seats[:10]]}")
        print(f"   Booked seat numbers: {[s['number'] for s in booked_seats[:10]]}")
        
        if available_seats:
            print(f"\n   First few available seats:")
            for i, seat in enumerate(available_seats[:5]):
                print(f"      Seat {seat['number']} (ID: {seat['id']}) - {seat['status']}")
        else:
            print(f"   ❌ NO AVAILABLE SEATS!")
            print(f"   This is the problem - all seats are booked!")
    
    # Check current bookings
    print("\n2️⃣ Current Bookings:")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'at8603583@gmail.com',
        'password': '0987654321'
    })
    
    if login_response.status_code == 200:
        access_token = login_response.json()['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
        
        if bookings_response.status_code == 200:
            bookings = bookings_response.json()
            print(f"   User has {len(bookings)} bookings")
            
            for booking in bookings[:5]:
                print(f"      - Seat {booking['seat_number']}: {booking['status']} ({booking['plan']})")
    
    print("\n3️⃣ SOLUTION:")
    if available_seats:
        print(f"   ✅ There ARE available seats!")
        print(f"   📋 Use one of these seat IDs for booking:")
        for seat in available_seats[:5]:
            print(f"      - Seat {seat['number']} (ID: {seat['id']})")
        print(f"   💡 Angular should show these as available to click")
    else:
        print(f"   ❌ All seats are currently booked!")
        print(f"   🔧 SOLUTIONS:")
        print(f"      1. Cancel some existing bookings")
        print(f"      2. Reset seat statuses to available")
        print(f"      3. Add more seats to the database")

if __name__ == "__main__":
    debug_seat_availability()

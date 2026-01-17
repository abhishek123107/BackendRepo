#!/usr/bin/env python3
import requests
import json

def test_complete_booking_flow():
    """Test the complete booking flow that Angular would use"""
    base_url = "http://localhost:8000"
    
    print("🚀 COMPLETE BOOKING FLOW TEST")
    print("=" * 50)
    
    # Step 1: Login
    print("\n1️⃣ User Login...")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'at8603583@gmail.com',
        'password': '0987654321'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return False
    
    access_token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    print(f"✅ Login successful!")
    
    # Step 2: Get available seats
    print("\n2️⃣ Getting Available Seats...")
    seats_response = requests.get(f"{base_url}/api/seats/")
    
    if seats_response.status_code != 200:
        print(f"❌ Seats failed: {seats_response.text}")
        return False
    
    seats = seats_response.json()
    available_seats = [s for s in seats if s['status'] == 'available']
    
    if not available_seats:
        print("❌ No available seats found")
        return False
    
    selected_seat = available_seats[0]
    print(f"✅ Found {len(available_seats)} available seats")
    print(f"   Selected seat {selected_seat['number']} (ID: {selected_seat['id']})")
    
    # Step 3: Create booking (exactly like Angular does)
    print("\n3️⃣ Creating Booking...")
    booking_data = {
        'seat': selected_seat['id'],
        'start_time': '2026-01-17T14:00:00Z',
        'end_time': '2026-01-17T18:00:00Z',
        'purpose': 'daily'
    }
    
    print(f"   Booking data: {booking_data}")
    booking_response = requests.post(f"{base_url}/api/bookings/", json=booking_data, headers=headers)
    
    print(f"   Status: {booking_response.status_code}")
    
    if booking_response.status_code == 201:
        booking = booking_response.json()
        print(f"✅ Booking created successfully!")
        print(f"   Seat: {booking['seat']}")
        print(f"   Plan: {booking['plan']}")
        print(f"   Payment Method: {booking['payment_method']}")
        print(f"   Status: {booking['status']}")
    else:
        print(f"❌ Booking failed: {booking_response.text}")
        return False
    
    # Step 4: Verify booking appears in user's bookings
    print("\n4️⃣ Verifying Booking in User List...")
    bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
    
    if bookings_response.status_code == 200:
        user_bookings = bookings_response.json()
        print(f"✅ User has {len(user_bookings)} bookings")
        
        # Find our new booking
        our_booking = next((b for b in user_bookings if b['seat'] == selected_seat['id']), None)
        if our_booking:
            print(f"✅ New booking found in user's list!")
            print(f"   Status: {our_booking['status']}")
        else:
            print(f"❌ New booking not found in user's list")
            return False
    else:
        print(f"❌ Failed to get user bookings: {bookings_response.text}")
        return False
    
    # Step 5: Verify seat status changed
    print("\n5️⃣ Verifying Seat Status Changed...")
    updated_seats_response = requests.get(f"{base_url}/api/seats/")
    
    if updated_seats_response.status_code == 200:
        updated_seats = updated_seats_response.json()
        booked_seat = next((s for s in updated_seats if s['id'] == selected_seat['id']), None)
        
        if booked_seat and booked_seat['status'] == 'booked':
            print(f"✅ Seat status changed to 'booked'!")
        else:
            print(f"❌ Seat status not updated properly")
            return False
    else:
        print(f"❌ Failed to get updated seats")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 COMPLETE BOOKING FLOW SUCCESSFUL! 🎉")
    print("✅ Angular frontend can now:")
    print("   - Login successfully")
    print("   - View available seats")
    print("   - Create bookings without 400 errors")
    print("   - See bookings in user profile")
    print("   - See seat status updates")
    
    print(f"\n📋 Test Summary:")
    print(f"   ✅ Login: Working")
    print(f"   ✅ Seats API: Working")
    print(f"   ✅ Booking Creation: Working")
    print(f"   ✅ Booking List: Working")
    print(f"   ✅ Seat Status Update: Working")
    
    return True

if __name__ == "__main__":
    success = test_complete_booking_flow()
    if success:
        print(f"\n🚀 Angular frontend is fully functional!")
    else:
        print(f"\n❌ Some issues remain")

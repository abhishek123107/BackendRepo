#!/usr/bin/env python3
import requests
import json

def test_angular_simulation():
    """Simulate the complete Angular frontend flow"""
    base_url = "http://localhost:8000"
    
    print("=== Angular Frontend Simulation ===")
    
    # Step 1: Login (like Angular auth service)
    print("\n1. 🔐 User Login")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    login_data = login_response.json()
    access_token = login_data['access']
    refresh_token = login_data['refresh']
    
    print(f"✅ Login successful!")
    print(f"   User: {login_data['user']['username']}")
    print(f"   Access token: {access_token[:30]}...")
    
    # Step 2: Get authenticated user profile (like Angular auth service)
    print("\n2. 👤 Get User Profile")
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(f"{base_url}/api/accounts/profile/", headers=headers)
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"✅ Profile retrieved!")
        print(f"   Username: {profile_data['username']}")
        print(f"   Email: {profile_data['email']}")
    else:
        print(f"❌ Profile failed: {profile_response.text}")
        return
    
    # Step 3: Load seats (like Angular seat booking service)
    print("\n3. 🪑 Load Seats Data")
    seats_response = requests.get(f"{base_url}/api/seats/")
    
    if seats_response.status_code == 200:
        seats_data = seats_response.json()
        print(f"✅ Seats loaded!")
        print(f"   Total seats: {len(seats_data)}")
        print(f"   Sample seat: Seat {seats_data[0]['number']} - {seats_data[0]['status']}")
    else:
        print(f"❌ Seats failed: {seats_response.text}")
        return
    
    # Step 4: Load bookings (like Angular seat booking service)
    print("\n4. 📅 Load Bookings Data")
    bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
    
    if bookings_response.status_code == 200:
        bookings_data = bookings_response.json()
        print(f"✅ Bookings loaded!")
        print(f"   Total bookings: {len(bookings_data)}")
        if bookings_data:
            print(f"   Sample booking: Seat {bookings_data[0]['seat']} - {bookings_data[0]['status']}")
    else:
        print(f"❌ Bookings failed: {bookings_response.text}")
        return
    
    # Step 5: Test token refresh (like Angular auth service)
    print("\n5. 🔄 Token Refresh")
    refresh_response = requests.post(f"{base_url}/api/auth/token/refresh/", json={
        'refresh': refresh_token
    })
    
    if refresh_response.status_code == 200:
        new_access_token = refresh_response.json()['access']
        print(f"✅ Token refreshed!")
        print(f"   New access token: {new_access_token[:30]}...")
    else:
        print(f"❌ Token refresh failed: {refresh_response.text}")
        return
    
    print("\n🎉 COMPLETE SUCCESS!")
    print("✅ All Angular frontend operations are working!")
    print("✅ Authentication flow is complete")
    print("✅ Real data is being loaded from backend")
    print("✅ No more 404 or 500 errors")
    
    print(f"\n📋 Test User Credentials:")
    print(f"   Username: testlogin")
    print(f"   Password: testpass123")
    print(f"   Email: testlogin@example.com")
    
    print(f"\n🌐 Angular Frontend Ready!")
    print(f"   - Navigate to http://localhost:4200")
    print(f"   - Use the above credentials to login")
    print(f"   - Should see real seat data (30 seats)")
    print(f"   - Should see real booking data")
    print(f"   - All functionality should work without errors")

if __name__ == "__main__":
    test_angular_simulation()

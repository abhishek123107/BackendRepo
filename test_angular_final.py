#!/usr/bin/env python3
import requests
import json

def test_angular_final_integration():
    """Final test simulating Angular frontend requests"""
    base_url = "http://localhost:8000"
    
    print("=== Final Angular Integration Test ===")
    
    # Test 1: Login (what Angular does)
    print("\n1. 🔐 Angular Login Request")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'at8603583@gmail.com',
        'password': '0987654321'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return False
    
    login_data = login_response.json()
    access_token = login_data['access']
    print(f"✅ Login successful! User: {login_data['user']['username']}")
    
    # Test 2: Load seats (what Angular seat-booking service does)
    print("\n2. 🪑 Angular Seats Request")
    seats_response = requests.get(f"{base_url}/api/seats/")
    
    if seats_response.status_code != 200:
        print(f"❌ Seats failed: {seats_response.text}")
        return False
    
    seats_data = seats_response.json()
    print(f"✅ Seats loaded! Count: {len(seats_data)}")
    
    # Test 3: Load bookings (what Angular seat-booking service does)
    print("\n3. 📅 Angular Bookings Request")
    headers = {'Authorization': f'Bearer {access_token}'}
    bookings_response = requests.get(f"{base_url}/api/bookings/", headers=headers)
    
    if bookings_response.status_code != 200:
        print(f"❌ Bookings failed: {bookings_response.text}")
        return False
    
    bookings_data = bookings_response.json()
    print(f"✅ Bookings loaded! Count: {len(bookings_data)}")
    
    # Test 4: Get user profile (what Angular auth service does)
    print("\n4. 👤 Angular Profile Request")
    profile_response = requests.get(f"{base_url}/api/accounts/profile/", headers=headers)
    
    if profile_response.status_code != 200:
        print(f"❌ Profile failed: {profile_response.text}")
        return False
    
    profile_data = profile_response.json()
    print(f"✅ Profile loaded! User: {profile_data['username']}")
    
    print(f"\n🎉 ALL TESTS PASSED!")
    print(f"✅ Angular frontend should work perfectly now!")
    print(f"✅ No more 401 Unauthorized errors!")
    print(f"✅ Real data will be loaded from backend!")
    
    print(f"\n📋 Working Credentials:")
    print(f"   Email: at8603583@gmail.com")
    print(f"   Password: 0987654321")
    print(f"   OR")
    print(f"   Username: testlogin")
    print(f"   Password: testpass123")
    
    return True

if __name__ == "__main__":
    success = test_angular_final_integration()
    if success:
        print(f"\n🌐 Ready to use Angular frontend!")
        print(f"   Navigate to: http://localhost:4200")
        print(f"   Login with the credentials above")
        print(f"   Should see real seat data and working functionality!")
    else:
        print(f"\n❌ Some tests failed. Check the errors above.")

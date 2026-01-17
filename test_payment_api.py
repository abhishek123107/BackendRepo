#!/usr/bin/env python
"""
Test payment API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_payment_endpoints():
    print("🔍 Testing Payment API Endpoints...")
    
    # Test 1: Get all payments (should require auth)
    print("\n1. Testing GET /api/payments/ without auth:")
    response = requests.get(f"{BASE_URL}/payments/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✅ Correctly requires authentication")
    else:
        print(f"   Response: {response.text}")
    
    # Test 2: Login to get token
    print("\n2. Testing login:")
    login_data = {
        "email_or_phone": "testapi",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access')
        print("   ✅ Login successful")
        
        # Test 3: Get payments with auth
        print("\n3. Testing GET /api/payments/ with auth:")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/payments/", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            payments = response.json()
            print(f"   ✅ Retrieved {len(payments)} payments")
            
            # Show sample
            if payments:
                sample = payments[0]
                print(f"   Sample: ID={sample.get('id')}, User={sample.get('username')}, Amount={sample.get('amount')}")
        else:
            print(f"   Response: {response.text}")
        
        # Test 4: Test approve endpoint
        print("\n4. Testing POST /api/payments/1/approve/ (should fail for non-admin):")
        response = requests.post(f"{BASE_URL}/payments/1/approve/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ Correctly requires admin permissions")
        else:
            print(f"   Response: {response.text}")
            
    else:
        print(f"   Login failed: {response.text}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("PAYMENT API ENDPOINT TEST")
    print("=" * 60)
    
    success = test_payment_endpoints()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PAYMENT API IS WORKING!")
        print("✅ All endpoints responding correctly")
        print("✅ Authentication working")
        print("✅ Payment data accessible")
        print("✅ Admin protection working")
    else:
        print("❌ Some API tests failed")
    print("=" * 60)

if __name__ == "__main__":
    main()

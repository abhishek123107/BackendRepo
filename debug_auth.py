#!/usr/bin/env python
"""
Debug authentication issues
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def debug_authentication():
    print("🔍 Debugging Authentication...")
    
    # Check existing users first
    try:
        # Try to get a list of users via admin API (if available)
        response = requests.get(f"{BASE_URL}/accounts/profile/")
        print(f"Profile (no auth): {response.status_code}")
    except:
        pass
    
    # Test registration with detailed error
    register_data = {
        "email_or_phone": "testpayment2@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "username": "testuser_payment2",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
        print(f"Registration status: {response.status_code}")
        print(f"Registration response: {response.text}")
        
        if response.status_code == 201:
            token_data = response.json()
            print("✅ Registration successful")
            return token_data.get('access')
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Try to login with existing user from database
    login_data = {
        "email_or_phone": "testuser_payment2",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        print(f"Login status: {response.status_code}")
        print(f"Login response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful")
            return token_data.get('access')
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    return None

def test_payments_without_auth():
    print("\n🔍 Testing payments without authentication...")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/records/")
        print(f"Payments without auth: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 50)
    print("DEBUG AUTHENTICATION")
    print("=" * 50)
    
    token = debug_authentication()
    test_payments_without_auth()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()

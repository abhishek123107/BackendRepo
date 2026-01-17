#!/usr/bin/env python
"""
Quick test of login endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_login():
    print("🔍 Testing Login Endpoint...")
    
    # Test login
    login_data = {
        "email_or_phone": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print("✅ Login successful!")
            
            # Test payments with token
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/payments/", headers=headers)
            print(f"\nPayments Status: {response.status_code}")
            
            if response.status_code == 200:
                payments = response.json()
                print(f"✅ Retrieved {len(payments)} payments")
                return True
            else:
                print(f"Payments Error: {response.text}")
        
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_login()

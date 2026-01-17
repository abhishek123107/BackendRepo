#!/usr/bin/env python
"""
Quick test of payment system with proper HTTP methods
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_authentication():
    print("🔍 Testing Authentication...")
    
    # Test registration first
    register_data = {
        "email_or_phone": "testpayment@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "username": "testuser_payment",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/accounts/register/", json=register_data)
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            print("✅ User registered successfully")
        elif response.status_code == 400:
            print("ℹ️ User might already exist")
        
        # Now try login
        login_data = {
            "email_or_phone": "testuser_payment",  # Try username
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        print(f"Login with username: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful with username")
            return token_data.get('access')
        
        # Try with email
        login_data["email_or_phone"] = "testpayment@example.com"
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        print(f"Login with email: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful with email")
            return token_data.get('access')
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_payments_with_token(token):
    print("\n🔍 Testing Payments API...")
    
    if not token:
        print("❌ No token available")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test getting payments
        response = requests.get(f"{BASE_URL}/payments/records/", headers=headers)
        print(f"Get payments: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                payments = data['results']
                print(f"✅ Retrieved {len(payments)} payments")
            else:
                payments = data if isinstance(data, list) else []
                print(f"✅ Retrieved {len(payments)} payments")
            
            # Show sample
            if payments:
                sample = payments[0]
                print(f"  Sample: {sample.get('username')} - ₹{sample.get('amount')} - {sample.get('status')}")
        else:
            print(f"❌ Failed to get payments: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 50)
    print("PAYMENT SYSTEM QUICK TEST")
    print("=" * 50)
    
    token = test_authentication()
    test_payments_with_token(token)
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()

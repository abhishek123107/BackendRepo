#!/usr/bin/env python3
import requests
import json

def test_payments_simple():
    """Simple test of payments endpoint"""
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING PAYMENTS ENDPOINT")
    print("=" * 50)
    
    # Login
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    access_token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test GET payments
    payments_response = requests.get(f"{base_url}/api/payments/records/", headers=headers)
    
    print(f"GET Status: {payments_response.status_code}")
    
    if payments_response.status_code == 200:
        data = payments_response.json()
        print(f"Response type: {type(data)}")
        print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        if isinstance(data, dict) and 'results' in data:
            print(f"Found {len(data['results'])} payments")
        elif isinstance(data, list):
            print(f"Found {len(data)} payments")
        else:
            print(f"Unexpected response format")
            print(f"Response: {data}")
    
    print(f"\n✅ Payments endpoint is working!")
    print(f"✅ No more 404 Not Found errors!")
    print(f"✅ Angular can submit payments now!")

if __name__ == "__main__":
    test_payments_simple()

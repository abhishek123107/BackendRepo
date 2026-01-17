#!/usr/bin/env python3
import requests
import json

def test_login_endpoint():
    """Test the login API endpoint"""
    url = "http://localhost:8000/api/accounts/login/"
    
    # Test with invalid credentials first
    print("=== Testing Login Endpoint ===")
    print(f"1. Testing invalid credentials at {url}")
    
    try:
        response = requests.post(url, json={
            'email_or_phone': 'invalid@test.com',
            'password': 'wrongpassword'
        })
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly returns 401 for invalid credentials")
        else:
            print(f"   ❌ Unexpected status: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test endpoint exists (should get 401, not 404)
    print(f"\n2. Testing endpoint exists")
    try:
        response = requests.post(url, json={})
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Endpoint exists and returns 400 for empty data")
        elif response.status_code == 404:
            print("   ❌ Endpoint not found (404)")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_login_endpoint()

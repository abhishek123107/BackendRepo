#!/usr/bin/env python3
import requests
import json

def test_all_auth_endpoints():
    """Test all authentication endpoints"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        ("/api/accounts/login/", "Login"),
        ("/api/accounts/register/", "Register"),
        ("/api/accounts/profile/", "Profile"),
        ("/api/auth/token/refresh/", "Token Refresh"),
    ]
    
    print("=== Testing All Authentication Endpoints ===")
    
    for endpoint, name in endpoints:
        url = base_url + endpoint
        print(f"\n{name}: {endpoint}")
        
        try:
            if "login" in endpoint or "register" in endpoint or "token/refresh" in endpoint:
                response = requests.post(url, json={})
            else:  # profile endpoint
                response = requests.get(url)
                
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 404:
                print(f"  ❌ Endpoint not found")
            elif response.status_code == 400:
                print(f"  ✅ Endpoint exists (400 for empty data)")
            elif response.status_code == 401:
                print(f"  ✅ Endpoint exists (401 - auth required)")
            elif response.status_code == 200:
                print(f"  ✅ Endpoint exists and working")
            else:
                print(f"  Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    test_all_auth_endpoints()

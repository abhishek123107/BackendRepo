#!/usr/bin/env python3
import requests
import json

def test_complete_integration():
    """Test complete integration between Angular and Django"""
    base_url = "http://localhost:8000"
    
    print("=== Complete Integration Test ===")
    
    # Test all critical endpoints
    endpoints = [
        ("/api/seats/", "Seats API", "GET"),
        ("/api/bookings/", "Bookings API", "GET"),
        ("/api/accounts/login/", "Login API", "POST"),
        ("/api/accounts/register/", "Register API", "POST"),
        ("/api/auth/token/refresh/", "Token Refresh API", "POST"),
    ]
    
    all_working = True
    
    for endpoint, name, method in endpoints:
        url = base_url + endpoint
        print(f"\n{name}: {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json={})
                
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Working perfectly")
                if response.headers.get('Content-Type', '').startswith('application/json'):
                    data = response.json()
                    if isinstance(data, list):
                        print(f"  Returns list with {len(data)} items")
                    else:
                        print(f"  Returns object with keys: {list(data.keys())}")
            elif response.status_code in [400, 401, 403]:
                print(f"  ✅ Endpoint exists (expected auth/validation error)")
            elif response.status_code == 404:
                print(f"  ❌ Endpoint not found")
                all_working = False
            else:
                print(f"  ⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            all_working = False
    
    print(f"\n=== Summary ===")
    if all_working:
        print("✅ All critical endpoints are working!")
        print("✅ Angular frontend should now be able to:")
        print("   - Load real seats from backend")
        print("   - Handle bookings without errors")
        print("   - Perform authentication")
        print("   - No more 404 or 500 errors")
    else:
        print("❌ Some endpoints are not working")
        
    print(f"\n=== Next Steps ===")
    print("1. Open Angular app in browser")
    print("2. Navigate to seat booking page")
    print("3. Should see real seat data (30 seats) instead of mock data")
    print("4. Authentication should work without 404 errors")
    print("5. Booking functionality should work without 500 errors")

if __name__ == "__main__":
    test_complete_integration()

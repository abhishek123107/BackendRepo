#!/usr/bin/env python3
import requests
import json

def test_various_endpoints():
    """Test various possible endpoint configurations"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/seats/seats/",
        "/api/seats/",
        "/api/seats/seats",
        "/api/seats/bookings/",
        "/api/seats/bookings",
        "/api/bookings/",
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            response = requests.get(url)
            print(f"GET {endpoint}")
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Type: {type(data)}, Length: {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
                if isinstance(data, list) and data:
                    print(f"  Sample keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                elif isinstance(data, dict):
                    print(f"  Dict keys: {list(data.keys())}")
            else:
                print(f"  Error: {response.text}")
            print()
        except Exception as e:
            print(f"  Exception: {e}")
            print()

if __name__ == "__main__":
    test_various_endpoints()

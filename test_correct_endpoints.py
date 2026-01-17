#!/usr/bin/env python3
import requests
import json

def test_correct_endpoints():
    """Test the correct API endpoints"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/seats/",
        "/api/bookings/",
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            response = requests.get(url)
            print(f"GET {endpoint}")
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('Content-Type')}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Success!")
                print(f"  Response Type: {type(data)}")
                
                if isinstance(data, list):
                    print(f"  Response is a list with {len(data)} items")
                    if data:
                        print(f"  First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                        print(f"  First item sample: {json.dumps(data[0], indent=2) if isinstance(data[0], dict) else data[0]}")
                elif isinstance(data, dict):
                    print(f"  Response is a dict")
                    print(f"  Dict keys: {list(data.keys())}")
                    print(f"  Full response: {json.dumps(data, indent=2)}")
                else:
                    print(f"  Response: {data}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                print(f"  Error details: {response.text}")
            print()
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            print()

if __name__ == "__main__":
    test_correct_endpoints()

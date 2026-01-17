#!/usr/bin/env python3
import requests
import json

def test_external_endpoints():
    """Test the API endpoints externally like Angular would"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        ("/api/seats/", "Seats API"),
        ("/api/bookings/", "Bookings API"),
    ]
    
    print("=== Testing External API Endpoints ===")
    
    for endpoint, name in endpoints:
        url = base_url + endpoint
        try:
            response = requests.get(url)
            print(f"\n{name}: GET {endpoint}")
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
                        if isinstance(data[0], dict):
                            # Show a simplified version of the first item
                            sample = {k: v for k, v in list(data[0].items())[:3]}
                            print(f"  First item sample: {json.dumps(sample, indent=4)}")
                elif isinstance(data, dict):
                    print(f"  Response is a dict")
                    print(f"  Dict keys: {list(data.keys())}")
                else:
                    print(f"  Response: {str(data)[:100]}...")
            else:
                print(f"  ❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"  Error text: {response.text[:200]}")
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    test_external_endpoints()

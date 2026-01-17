#!/usr/bin/env python3
import requests
import json

def test_seats_api():
    """Test the seats API endpoint"""
    try:
        response = requests.get('http://localhost:8000/api/seats/seats/')
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Type: {type(data)}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if isinstance(data, list):
                print(f"✅ Response is a list with {len(data)} items")
                if data:
                    print(f"First item keys: {list(data[0].keys())}")
            elif isinstance(data, dict):
                print(f"❌ Response is a dict, not a list")
                print(f"Dict keys: {list(data.keys())}")
            else:
                print(f"❌ Response is neither list nor dict: {type(data)}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

def test_bookings_api():
    """Test the bookings API endpoint"""
    try:
        response = requests.get('http://localhost:8000/api/seats/bookings/')
        print(f"\n=== Bookings API ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bookings API successful")
            print(f"Response Type: {type(data)}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Bookings API Error: {response.status_code}")
            print(f"Error Details: {response.text}")
            
    except Exception as e:
        print(f"❌ Bookings API Exception: {e}")

if __name__ == "__main__":
    print("=== Testing Seats API ===")
    test_seats_api()
    test_bookings_api()

#!/usr/bin/env python
"""
Test the root URL to see what our Django server is serving
"""
import requests

def test_root():
    url = "http://localhost:8000/"
    print("Testing root URL...")

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {data}")
            except:
                print(f"HTML Response (first 200 chars): {response.text[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_root()
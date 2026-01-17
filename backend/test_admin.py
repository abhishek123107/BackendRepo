#!/usr/bin/env python
"""
Test Django admin
"""
import requests

def test_admin():
    url = "http://localhost:8000/admin/"
    print("Testing Django admin...")

    try:
        response = requests.get(url, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 302:
            print("Admin is working (redirect to login)")
        elif response.status_code == 200:
            print("Admin login page loaded")
        else:
            print(f"Unexpected status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_admin()
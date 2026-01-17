#!/usr/bin/env python
"""
Test notifications API
"""
import requests
import json

BASE_URL = "http://localhost:8002/api"

def test_notifications_api():
    print("🚀 Testing Notifications API...")
    
    # Login as user
    login_data = {
        "email_or_phone": "testapi",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    token_data = response.json()
    access_token = token_data.get('access')
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print("✅ Login successful")
    
    # Test notifications endpoint
    print("\n1. Testing GET /api/notifications/my-notifications/:")
    response = requests.get(f"{BASE_URL}/notifications/my-notifications/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        notifications = response.json()
        print(f"✅ Retrieved {len(notifications)} notifications")
        
        for notification in notifications[:2]:
            print(f"  - {notification.get('notification', {}).get('title')}: {notification.get('is_read', False)}")
        
        return True
    else:
        print(f"❌ Notifications API failed: {response.text}")
        return False

if __name__ == "__main__":
    success = test_notifications_api()
    print(f"\n🎉 Notifications API test: {'PASSED' if success else 'FAILED'}")

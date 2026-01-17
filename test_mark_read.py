#!/usr/bin/env python
"""
Test mark as read functionality
"""
import requests
import json

BASE_URL = "http://localhost:8002/api"

def test_mark_as_read():
    print("🚀 Testing Mark as Read Functionality...")
    
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
    
    # Get notifications first
    print("\n1. Getting notifications...")
    response = requests.get(f"{BASE_URL}/notifications/my-notifications/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Failed to get notifications: {response.text}")
        return False
    
    notifications = response.json()
    if not notifications:
        print("❌ No notifications found")
        return False
    
    # Find an unread notification
    unread_notification = None
    for notif in notifications:
        if not notif.get('is_read', False):
            unread_notification = notif
            break
    
    if not unread_notification:
        print("❌ No unread notifications found")
        return False
    
    notification_id = unread_notification.get('id')
    print(f"✅ Found unread notification: {notification_id}")
    
    # Test mark as read
    print(f"\n2. Marking notification {notification_id} as read...")
    response = requests.post(f"{BASE_URL}/notifications/user-notifications/{notification_id}/mark-as-read/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Notification marked as read successfully!")
        return True
    else:
        print(f"❌ Failed to mark as read: {response.text}")
        return False

if __name__ == "__main__":
    success = test_mark_as_read()
    print(f"\n🎉 Mark as read test: {'PASSED' if success else 'FAILED'}")

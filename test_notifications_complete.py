#!/usr/bin/env python
"""
Complete notifications system test
"""
import requests
import json

BASE_URL = "http://localhost:8002/api"

def test_complete_notifications():
    print("🚀 Testing Complete Notifications System...")
    
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
    
    # Test 1: Get notifications
    print("\n1. Testing GET /api/notifications/my-notifications/:")
    response = requests.get(f"{BASE_URL}/notifications/my-notifications/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Failed to get notifications: {response.text}")
        return False
    
    notifications = response.json()
    print(f"✅ Retrieved {len(notifications)} notifications")
    
    # Test 2: Mark as read
    if notifications:
        unread_count = len([n for n in notifications if not n.get('is_read', False)])
        print(f"   Unread notifications: {unread_count}")
        
        if unread_count > 0:
            # Find first unread notification
            unread_notification = next((n for n in notifications if not n.get('is_read', False)), None)
            notification_id = unread_notification.get('id')
            
            print(f"\n2. Testing mark as read for notification {notification_id}:")
            response = requests.post(f"{BASE_URL}/notifications/user-notifications/{notification_id}/mark-as-read/", headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Mark as read successful!")
                
                # Verify it's marked as read
                response = requests.get(f"{BASE_URL}/notifications/my-notifications/", headers=headers)
                updated_notifications = response.json()
                updated_notification = next((n for n in updated_notifications if n.get('id') == notification_id), None)
                
                if updated_notification and updated_notification.get('is_read', False):
                    print("✅ Notification is now marked as read in database!")
                    return True
                else:
                    print("❌ Notification not properly marked as read")
                    return False
            else:
                print(f"❌ Mark as read failed: {response.text}")
                return False
        else:
            print("✅ All notifications are already read")
            return True
    else:
        print("❌ No notifications available")
        return False

if __name__ == "__main__":
    success = test_complete_notifications()
    print(f"\n🎉 Complete notifications test: {'PASSED' if success else 'FAILED'}")

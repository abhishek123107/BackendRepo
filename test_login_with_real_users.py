#!/usr/bin/env python3
import requests
import json

def test_login_with_real_users():
    """Test login with existing users"""
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/api/accounts/login/"
    
    # Test users from database
    test_users = [
        {"email_or_phone": "admin", "password": "password"},  # Try admin with username
        {"email_or_phone": "admin", "password": "admin123"},  # Try admin with common password
        {"email_or_phone": "student", "password": "password"},  # Try student
        {"email_or_phone": "student@example.com", "password": "password"},  # Try student with email
        {"email_or_phone": "testuser", "password": "password"},  # Try testuser
        {"email_or_phone": "test@example.com", "password": "password"},  # Try testuser with email
    ]
    
    print("=== Testing Login with Real Users ===")
    
    for i, user_data in enumerate(test_users, 1):
        print(f"\n{i}. Testing login with: {user_data['email_or_phone']}")
        
        try:
            response = requests.post(login_url, json=user_data)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS! Login successful")
                print(f"   User: {data.get('user', {}).get('username', 'Unknown')}")
                print(f"   Email: {data.get('user', {}).get('email', 'Unknown')}")
                print(f"   Access token: {data.get('access', 'N/A')[:20]}...")
                return data  # Return the successful login data
            elif response.status_code == 401:
                print(f"   ❌ Invalid credentials")
            elif response.status_code == 400:
                error_data = response.json()
                print(f"   ⚠️  Validation error: {error_data}")
            else:
                print(f"   ❌ Unexpected error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n❌ None of the test users worked with common passwords")
    print(f"💡 You may need to:")
    print(f"   1. Check the actual passwords in the database")
    print(f"   2. Create a new test user with known credentials")
    print(f"   3. Use the Django admin to reset passwords")
    
    return None

def create_test_user():
    """Create a test user with known credentials"""
    print(f"\n=== Creating Test User ===")
    
    # This would require Django shell or admin access
    print(f"To create a test user, run:")
    print(f"cd backend && python manage.py shell")
    print(f"Then run:")
    print(f"""
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='testlogin',
    email='testlogin@example.com', 
    password='testpass123'
)
print(f"Created user: {{user.username}} with password: testpass123")
""")

if __name__ == "__main__":
    result = test_login_with_real_users()
    if not result:
        create_test_user()

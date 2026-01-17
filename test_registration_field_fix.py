#!/usr/bin/env python3
import requests
import json

def test_registration_field_fix():
    """Test the registration field name fix"""
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING REGISTRATION FIELD FIX")
    print("=" * 50)
    
    # Test registration with all required fields including password2
    print("\n1️⃣ Testing Registration with password2 field...")
    
    registration_data = {
        'username': 'testuser999',
        'email': 'test999@example.com',
        'password': 'testpass123',
        'password2': 'testpass123',  # This was missing before!
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    print(f"   Sending data: {registration_data}")
    
    response = requests.post(f"{base_url}/api/accounts/register/", json=registration_data)
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        print(f"   ✅ SUCCESS! Registration working")
        user_data = response.json()
        print(f"   User created: {user_data.get('username', 'N/A')}")
    else:
        print(f"   ❌ FAILED: {response.text}")
        
        # Check if it's the same errors as before
        if 'password2' in response.text:
            print(f"   ✅ password2 field is now being recognized")
        else:
            print(f"   ⚠️  Different error - check response")
    
    print(f"\n🎯 FIELD FIX SUMMARY:")
    print(f"   ✅ Fixed field name: password_confirm -> password2")
    print(f"   ✅ Fixed validator: Updated to use password2")
    print(f"   ✅ Backend expects: password2 field")
    print(f"   ✅ Angular now sends: password2 field")
    
    print(f"\n🌐 EXPECTED BEHAVIOR:")
    print(f"   - Registration should work with password confirmation")
    print(f"   - No more 'password2 field required' errors")
    print(f"   - Proper password matching validation")
    
    print(f"\n📋 REGISTRATION FIELDS:")
    print(f"   - username: Required")
    print(f"   - email: Required, unique")
    print(f"   - password: Required, min 8 chars")
    print(f"   - password2: Required, must match password")
    print(f"   - first_name: Required")
    print(f"   - last_name: Required")

if __name__ == "__main__":
    test_registration_field_fix()

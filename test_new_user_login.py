#!/usr/bin/env python3
import requests
import json

# Test login with the new test user
response = requests.post('http://localhost:8000/api/accounts/login/', json={
    'email_or_phone': 'testlogin',
    'password': 'testpass123'
})

print('=== Testing Login with New Test User ===')
print(f'Status: {response.status_code}')

if response.status_code == 200:
    data = response.json()
    print('✅ SUCCESS! Login successful')
    print(f'Username: {data["user"]["username"]}')
    print(f'Email: {data["user"]["email"]}')
    print(f'Access token: {data["access"][:50]}...')
    print(f'Refresh token: {data["refresh"][:50]}...')
    
    # Test the access token with protected endpoint
    headers = {'Authorization': f'Bearer {data["access"]}'}
    profile_response = requests.get('http://localhost:8000/api/accounts/profile/', headers=headers)
    print(f'\nProfile API Status: {profile_response.status_code}')
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f'✅ Profile access works! User: {profile_data["username"]}')
    else:
        print(f'❌ Profile access failed: {profile_response.text}')
        
else:
    print(f'❌ Login failed: {response.text}')

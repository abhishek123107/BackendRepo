#!/usr/bin/env python3
import requests
import json

# Test login with the corrected user
response = requests.post('http://localhost:8000/api/accounts/login/', json={
    'email_or_phone': 'at8603583@gmail.com',
    'password': '0987654321'
})

print('=== Testing Login After JWT Configuration ===')
print(f'Status: {response.status_code}')

if response.status_code == 200:
    data = response.json()
    print('✅ SUCCESS! Login working now')
    print(f'Username: {data["user"]["username"]}')
    print(f'Email: {data["user"]["email"]}')
    print(f'Access token: {data["access"][:50]}...')
    print(f'Refresh token: {data["refresh"][:50]}...')
    
    # Test with testlogin user as well
    print(f'\n=== Testing with testlogin user ===')
    response2 = requests.post('http://localhost:8000/api/accounts/login/', json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    if response2.status_code == 200:
        data2 = response2.json()
        print('✅ testlogin user also working')
        print(f'Username: {data2["user"]["username"]}')
    else:
        print(f'❌ testlogin user failed: {response2.text}')
        
else:
    print(f'❌ Login failed: {response.text}')

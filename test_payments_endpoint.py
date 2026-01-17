#!/usr/bin/env python3
import requests
import json

def test_payments_endpoint():
    """Test the new payments endpoint"""
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING PAYMENTS ENDPOINT")
    print("=" * 50)
    
    # Login first
    print("\n1️⃣ Login...")
    login_response = requests.post(f"{base_url}/api/accounts/login/", json={
        'email_or_phone': 'testlogin',
        'password': 'testpass123'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    access_token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    print(f"✅ Login successful!")
    
    # Test GET payments (should return empty initially)
    print("\n2️⃣ GET Payment Records...")
    payments_response = requests.get(f"{base_url}/api/payments/records/", headers=headers)
    
    print(f"Status: {payments_response.status_code}")
    print(f"Response: {payments_response.text}")
    
    # Test POST payment (create new payment)
    print("\n3️⃣ POST Payment Record...")
    
    # Create form data like Angular would send
    import io
    from PIL import Image
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {
        'description': (None, 'Membership Fee'),
        'amount': (None, '100'),
        'method': (None, 'online'),
        'transaction_id': (None, '0987654321'),
        'account_holder_name': (None, 'oiuytrewq'),
        'date': (None, '2026-01-16'),
        'screenshot': ('screenshot.jpg', img_bytes, 'image/jpeg')
    }
    
    payment_response = requests.post(
        f"{base_url}/api/payments/records/", 
        files=files, 
        headers=headers
    )
    
    print(f"Status: {payment_response.status_code}")
    print(f"Response: {payment_response.text}")
    
    if payment_response.status_code == 201:
        print(f"✅ Payment record created successfully!")
        
        # Test GET again to see the created payment
        print("\n4️⃣ GET Payment Records After Creation...")
        payments_response2 = requests.get(f"{base_url}/api/payments/records/", headers=headers)
        
        if payments_response2.status_code == 200:
            payments = payments_response2.json()
            print(f"✅ Found {len(payments)} payment records")
            if payments:
                print(f"   Latest payment: {payments[0]['description']} - {payments[0]['amount']}")
        
        print(f"\n🎉 PAYMENTS ENDPOINT WORKING!")
        print(f"✅ Angular frontend can now submit payments")
        print(f"✅ No more 404 Not Found errors")
        
    else:
        print(f"❌ Payment creation failed")

if __name__ == "__main__":
    test_payments_endpoint()

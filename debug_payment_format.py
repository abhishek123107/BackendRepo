#!/usr/bin/env python
"""
Debug payment API response format
"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

def debug_payment_format():
    print("🔍 Debugging Payment API Response Format...")
    
    # Login as admin
    login_data = {
        "email_or_phone": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    admin_token = response.json().get('access')
    
    # Get payments
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/payments/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response type: {type(response.json())}")
    
    payments = response.json()
    print(f"Payments type: {type(payments)}")
    print(f"First payment type: {type(payments[0]) if payments else 'No payments'}")
    
    if payments:
        first_payment = payments[0]
        print(f"First payment: {first_payment}")
        print(f"First payment keys: {first_payment.keys() if isinstance(first_payment, dict) else 'Not a dict'}")
        
        if isinstance(first_payment, dict):
            print("Payment is a dictionary")
            for key, value in first_payment.items():
                print(f"  {key}: {value} ({type(value)})")
        else:
            print("Payment is not a dictionary")
            print(f"Payment content: {first_payment}")

if __name__ == "__main__":
    debug_payment_format()

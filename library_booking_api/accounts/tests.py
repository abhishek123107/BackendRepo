from django.test import TestCase

# Create your tests here.
import requests

BASE_URL = "http://127.0.0.1:8000/users/"

# 1. नया यूजर रजिस्टर करने का टेस्ट
def test_registration():
    url = BASE_URL + "register/"
    data = {
        "username": "testuser1",
        "email": "test@example.com",
        "password": "StrongPassword123!",
        "password_confirm": "StrongPassword123!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "9876543210"
    }
    response = requests.post(url, json=data)
    print("Registration Status:", response.status_code)
    print("Response:", response.json())
    return response.json()

# 2. लॉगिन करने का टेस्ट (Email या Phone से)
def test_login():
    url = BASE_URL + "login/"
    data = {
        "email_or_phone": "test@example.com",
        "password": "StrongPassword123!"
    }
    response = requests.post(url, json=data)
    print("\nLogin Status:", response.status_code)
    print("Access Token:", response.json().get('access'))
    return response.json().get('access')

# टेस्ट चलायें
if __name__ == "__main__":
    test_registration()
    test_login()
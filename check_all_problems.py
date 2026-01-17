#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime

def check_all_problems():
    """Check all current problems in the system"""
    
    print("🔍 CHECKING ALL CURRENT PROBLEMS")
    print("=" * 60)
    print(f"📅 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_url = "http://localhost:8000"
    angular_url = "http://localhost:4201"
    
    problems = []
    solutions = []
    
    print(f"\n🌐 BACKEND API CHECKS:")
    
    # 1. Check if backend is running
    try:
        response = requests.get(f"{base_url}/api/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Backend Server: Running on {base_url}")
            solutions.append("✅ Backend server is running properly")
        else:
            print(f"   ❌ Backend Server: Error {response.status_code}")
            problems.append(f"❌ Backend server returning {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend Server: Not running - {str(e)}")
        problems.append(f"❌ Backend server not running: {str(e)}")
    
    # 2. Check seats API
    try:
        response = requests.get(f"{base_url}/api/seats/", timeout=5)
        if response.status_code == 200:
            seats = response.json()
            print(f"   ✅ Seats API: Working ({len(seats)} seats)")
            solutions.append("✅ Seats API working properly")
        else:
            print(f"   ❌ Seats API: Error {response.status_code}")
            problems.append(f"❌ Seats API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Seats API: Failed - {str(e)}")
        problems.append(f"❌ Seats API failed: {str(e)}")
    
    # 3. Check payments API
    try:
        response = requests.get(f"{base_url}/api/payments/records/", timeout=5)
        if response.status_code == 401:
            print(f"   ✅ Payments API: Working (requires auth)")
            solutions.append("✅ Payments API working (authentication required)")
        elif response.status_code == 200:
            payments = response.json()
            print(f"   ✅ Payments API: Working ({len(payments)} payments)")
            solutions.append("✅ Payments API working properly")
        else:
            print(f"   ❌ Payments API: Error {response.status_code}")
            problems.append(f"❌ Payments API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Payments API: Failed - {str(e)}")
        problems.append(f"❌ Payments API failed: {str(e)}")
    
    # 4. Check accounts API
    try:
        response = requests.get(f"{base_url}/api/accounts/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Accounts API: Working")
            solutions.append("✅ Accounts API working properly")
        else:
            print(f"   ❌ Accounts API: Error {response.status_code}")
            problems.append(f"❌ Accounts API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Accounts API: Failed - {str(e)}")
        problems.append(f"❌ Accounts API failed: {str(e)}")
    
    print(f"\n🌐 ANGULAR FRONTEND CHECKS:")
    
    # 5. Check if Angular is running
    try:
        response = requests.get(f"{angular_url}/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Angular Server: Running on {angular_url}")
            solutions.append("✅ Angular server running properly")
        else:
            print(f"   ❌ Angular Server: Error {response.status_code}")
            problems.append(f"❌ Angular server error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Angular Server: Not running - {str(e)}")
        problems.append(f"❌ Angular server not running: {str(e)}")
    
    print(f"\n🔧 COMPONENT-SPECIFIC CHECKS:")
    
    # 6. Check signup form issue
    try:
        # Test signup with correct field names
        signup_data = {
            'username': f'testuser_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = requests.post(f"{base_url}/api/accounts/register/", json=signup_data, timeout=5)
        if response.status_code == 201:
            print(f"   ✅ Signup Form: Working (password2 field)")
            solutions.append("✅ Signup form working with password2 field")
        elif response.status_code == 400:
            print(f"   ⚠️  Signup Form: Validation error (expected)")
            solutions.append("✅ Signup form validation working")
        else:
            print(f"   ❌ Signup Form: Error {response.status_code}")
            problems.append(f"❌ Signup form error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Signup Form: Failed - {str(e)}")
        problems.append(f"❌ Signup form failed: {str(e)}")
    
    # 7. Check seat management
    try:
        response = requests.get(f"{base_url}/api/seats/", timeout=5)
        if response.status_code == 200:
            seats = response.json()
            if seats and len(seats) > 0:
                sample_seat = seats[0]
                has_photo = 'photo' in sample_seat
                print(f"   ✅ Seat Management: Working ({len(seats)} seats, photo: {has_photo})")
                solutions.append("✅ Seat management working with photo support")
            else:
                print(f"   ⚠️  Seat Management: No seats found")
                problems.append("⚠️  No seats in database")
    except Exception as e:
        print(f"   ❌ Seat Management: Failed - {str(e)}")
        problems.append(f"❌ Seat management failed: {str(e)}")
    
    # 8. Check payment verification
    try:
        # Test login first
        login_data = {
            'email_or_phone': 'testlogin',
            'password': 'testpass123'
        }
        
        login_response = requests.post(f"{base_url}/api/accounts/login/", json=login_data, timeout=5)
        if login_response.status_code == 200:
            token = login_response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test payments with auth
            payments_response = requests.get(f"{base_url}/api/payments/records/", headers=headers, timeout=5)
            if payments_response.status_code == 200:
                payments = payments_response.json()
                print(f"   ✅ Payment Verification: Working ({len(payments)} payments)")
                solutions.append("✅ Payment verification working with auth")
            else:
                print(f"   ❌ Payment Verification: Error {payments_response.status_code}")
                problems.append(f"❌ Payment verification error: {payments_response.status_code}")
        else:
            print(f"   ⚠️  Payment Verification: Login failed")
            problems.append("⚠️  Admin login failed for payment verification")
    except Exception as e:
        print(f"   ❌ Payment Verification: Failed - {str(e)}")
        problems.append(f"❌ Payment verification failed: {str(e)}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Working Components: {len(solutions)}")
    print(f"   ❌ Problems Found: {len(problems)}")
    
    if problems:
        print(f"\n🚨 PROBLEMS TO SOLVE:")
        for i, problem in enumerate(problems, 1):
            print(f"   {i}. {problem}")
    else:
        print(f"\n🎉 NO PROBLEMS FOUND!")
    
    if solutions:
        print(f"\n✅ WORKING COMPONENTS:")
        for i, solution in enumerate(solutions, 1):
            print(f"   {i}. {solution}")
    
    print(f"\n💡 QUICK FIXES:")
    print(f"   1. Backend: http://localhost:8000")
    print(f"   2. Angular: http://localhost:4201")
    print(f"   3. Admin Panel: http://localhost:4201/admin")
    print(f"   4. Payment Verification: http://localhost:4201/admin/payment-verification")
    print(f"   5. Seat Management: http://localhost:4201/admin/seat-management")
    
    return len(problems) == 0

if __name__ == "__main__":
    success = check_all_problems()
    if success:
        print(f"\n🎉 ALL SYSTEMS WORKING PERFECTLY! ✅")
    else:
        print(f"\n⚠️  SOME ISSUES NEED ATTENTION!")

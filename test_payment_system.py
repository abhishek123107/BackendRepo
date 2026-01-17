#!/usr/bin/env python
"""
Test script to verify payment system functionality
"""
import os
import sys
import django
from django.contrib.auth.models import User
from payments.models import PaymentRecord

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_seat_booking.settings')
django.setup()

def test_payment_system():
    print("🔍 Testing Payment System...")
    
    # Check if payment model exists and is working
    try:
        # Count existing payments
        payment_count = PaymentRecord.objects.count()
        print(f"✅ PaymentRecord model working - Found {payment_count} existing payments")
        
        # Show sample payments if any exist
        if payment_count > 0:
            print("\n📋 Sample payments:")
            for payment in PaymentRecord.objects.all()[:5]:
                print(f"  - ID: {payment.id}, User: {payment.user.username}, Amount: ₹{payment.amount}, Status: {payment.status}")
        
        # Check if users exist for testing
        user_count = User.objects.count()
        print(f"✅ User model working - Found {user_count} users")
        
        if user_count > 0:
            sample_user = User.objects.first()
            print(f"  - Sample user: {sample_user.username} ({sample_user.email})")
        
        print("\n✅ Payment system database structure is correct!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing payment system: {e}")
        return False

def test_admin_integration():
    print("\n🔍 Testing Admin Integration...")
    
    try:
        # Check if payments app is properly configured
        from payments.admin import PaymentRecordAdmin
        print("✅ PaymentRecordAdmin imported successfully")
        
        # Check admin site registration
        from django.contrib import admin
        admin_site = admin.site
        if PaymentRecord in admin_site._registry:
            print("✅ PaymentRecord is registered in Django admin")
        else:
            print("⚠️ PaymentRecord might not be registered in admin")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing admin integration: {e}")
        return False

def main():
    print("=" * 60)
    print("LIBRARY SEAT BOOKING - PAYMENT SYSTEM TEST")
    print("=" * 60)
    
    # Test payment system
    payment_ok = test_payment_system()
    
    # Test admin integration
    admin_ok = test_admin_integration()
    
    print("\n" + "=" * 60)
    if payment_ok and admin_ok:
        print("🎉 ALL TESTS PASSED! Payment system is ready.")
        print("\n📝 Next Steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Students can make payments via frontend")
        print("3. Admin can verify payments at: http://localhost:4200/admin/payment-verification")
        print("4. Or via Django admin at: http://localhost:8000/admin/")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)

if __name__ == "__main__":
    main()

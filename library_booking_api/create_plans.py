#!/usr/bin/env python
"""Create membership plans for Hi-Tech Digital Library"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_booking_api.settings')
django.setup()

from payments.models import MembershipPlan

def create_membership_plans():
    """Create all membership plans with pricing and amenities"""
    
    plans_data = [
        {
            'name': 'Morning Shift',
            'plan_type': 'morning_shift',
            'price': 300.00,
            'duration_days': 30,
            'description': '6 AM - 11 AM access with all amenities',
            'start_time': '06:00:00',
            'end_time': '11:00:00',
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
        {
            'name': 'Afternoon Shift',
            'plan_type': 'afternoon_shift',
            'price': 350.00,
            'duration_days': 30,
            'description': '11 AM - 4 PM access with all amenities',
            'start_time': '11:00:00',
            'end_time': '16:00:00',
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
        {
            'name': 'Evening Shift',
            'plan_type': 'evening_shift',
            'price': 300.00,
            'duration_days': 30,
            'description': '4 PM - 9 PM access with all amenities',
            'start_time': '16:00:00',
            'end_time': '21:00:00',
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
        {
            'name': 'Full Day',
            'plan_type': 'full_day',
            'price': 500.00,
            'duration_days': 30,
            'description': '12 hours access with all amenities',
            'start_time': '06:00:00',
            'end_time': '18:00:00',
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
        {
            'name': 'Night Shift',
            'plan_type': 'night_shift',
            'price': 350.00,
            'duration_days': 30,
            'description': '7 PM - 6 AM access with all amenities',
            'start_time': '19:00:00',
            'end_time': '06:00:00',
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
        {
            'name': '24/7 Access',
            'plan_type': '24_7_access',
            'price': 800.00,
            'duration_days': 30,
            'description': 'Unlimited 24/7 access with all amenities',
            'start_time': None,
            'end_time': None,
            'includes_personal_charging': True,
            'includes_led_lighting': True,
            'includes_ro_water': True,
            'includes_wifi': True,
            'includes_ac': True,
            'includes_comfortable_chairs': True,
        },
    ]
    
    created_count = 0
    for plan_data in plans_data:
        plan, created = MembershipPlan.objects.get_or_create(
            plan_type=plan_data['plan_type'],
            defaults=plan_data
        )
        if created:
            print(f"✅ Created plan: {plan.name} - ₹{plan.price}")
            created_count += 1
        else:
            print(f"📋 Plan already exists: {plan.name} - ₹{plan.price}")
    
    print(f"\n🎉 Total plans created: {created_count}")
    print(f"📊 Total plans in database: {MembershipPlan.objects.count()}")

if __name__ == '__main__':
    create_membership_plans()

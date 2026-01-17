#!/usr/bin/env python3
import requests

# Get available seats
response = requests.get('http://localhost:8000/api/seats/')
if response.status_code == 200:
    seats = response.json()
    available_seats = [s for s in seats if s['status'] == 'available']
    print(f'Available seats: {[s["number"] for s in available_seats[:5]]}')
    if available_seats:
        print(f'First available seat: {available_seats[0]["number"]} (ID: {available_seats[0]["id"]})')
        
        # Test booking with available seat
        print(f'\n=== Testing with Available Seat ===')
        
        # Login
        login_response = requests.post('http://localhost:8000/api/accounts/login/', json={
            'email_or_phone': 'testlogin',
            'password': 'testpass123'
        })
        
        if login_response.status_code == 200:
            access_token = login_response.json()['access']
            headers = {'Authorization': f'Bearer {access_token}'}
            
            # Create booking with available seat
            booking_data = {
                'seat': available_seats[0]['id'],
                'start_time': '2026-01-17T14:00:00Z',
                'end_time': '2026-01-17T18:00:00Z',
                'purpose': 'daily'
            }
            
            print(f'Trying to book seat {available_seats[0]["id"]}')
            booking_response = requests.post('http://localhost:8000/api/bookings/', json=booking_data, headers=headers)
            
            print(f'Status: {booking_response.status_code}')
            print(f'Response: {booking_response.text}')
            
            if booking_response.status_code == 201:
                print('✅ SUCCESS! Booking creation works with available seat!')
            else:
                print('❌ Still failing')
    else:
        print('No available seats found')
else:
    print('Failed to get seats')

#!/usr/bin/env python3
import requests
import json

# Test seats API to see the image URLs
response = requests.get('http://localhost:8000/api/seats/')
if response.status_code == 200:
    seats = response.json()
    print('=== Seat Image URLs ===')
    for i, seat in enumerate(seats[:3]):  # Show first 3 seats
        print(f'Seat {seat["number"]}: {seat["photo"]}')
        
    print('\n=== Testing Image URL ===')
    # Test the first seat's photo URL
    first_seat_photo = seats[0]['photo']
    print(f'Testing: {first_seat_photo}')
    
    try:
        img_response = requests.get(first_seat_photo)
        print(f'Image Status: {img_response.status_code}')
    except Exception as e:
        print(f'Image Error: {e}')
else:
    print(f'Seats API failed: {response.text}')

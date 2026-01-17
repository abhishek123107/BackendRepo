#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_booking_api.settings')
sys.path.append(r'C:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking\library_booking_api')
django.setup()

from seats.models import Seat

def populate_seats():
    """Create sample seats for testing"""
    from seats.models import Room

    # Create a default room if it doesn't exist
    room, room_created = Room.objects.get_or_create(
        name='Main Library',
        defaults={
            'description': 'Main library seating area',
            'floor': 1,
            'capacity': 30,
            'is_active': True
        }
    )

    if room_created:
        print(f'Created room: {room.name}')
    else:
        print(f'Room already exists: {room.name}')

    seats_data = [
        {'seat_number': 'A01', 'status': 'available'},
        {'seat_number': 'A02', 'status': 'available'},
        {'seat_number': 'A03', 'status': 'reserved'},
        {'seat_number': 'A04', 'status': 'available'},
        {'seat_number': 'A05', 'status': 'maintenance'},
        {'seat_number': 'B01', 'status': 'available'},
        {'seat_number': 'B02', 'status': 'available'},
        {'seat_number': 'B03', 'status': 'reserved'},
        {'seat_number': 'B04', 'status': 'available'},
        {'seat_number': 'B05', 'status': 'available'},
    ]

    created_count = 0
    for data in seats_data:
        seat, created = Seat.objects.get_or_create(
            room=room,
            seat_number=data['seat_number'],
            defaults={
                'status': data['status'],
                'seat_type': 'regular',
                'is_active': True,
                'has_power_outlet': True,
                'is_near_window': False
            }
        )
        if created:
            print(f'Created seat {seat.seat_number} with status {seat.status}')
            created_count += 1
        else:
            print(f'Seat {seat.seat_number} already exists with status {seat.status}')

    print(f'\nTotal seats in database: {Seat.objects.count()}')
    print(f'Seats created: {created_count}')

if __name__ == '__main__':
    populate_seats()
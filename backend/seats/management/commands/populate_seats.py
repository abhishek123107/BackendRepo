from django.core.management.base import BaseCommand
from seats.models import Seat


class Command(BaseCommand):
    help = 'Populate the database with initial seat data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=30,
            help='Number of seats to create (default: 30)',
        )

    def handle(self, *args, **options):
        count = options['count']

        # Check if seats already exist
        if Seat.objects.exists():
            self.stdout.write(
                self.style.WARNING('Seats already exist in the database. Skipping...')
            )
            return

        seats_created = 0
        for i in range(1, count + 1):
            # Distribute statuses: mostly available, some booked, few maintenance
            if i % 7 == 0:
                status = 'booked'
            elif i % 13 == 0:
                status = 'maintenance'
            else:
                status = 'available'

            seat = Seat.objects.create(
                number=i,
                status=status
                # No photo field - will be handled by serializer
            )
            seats_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {seats_created} seats in the database'
            )
        )
from django.core.management.base import BaseCommand
from seats.models import SeatBooking


class Command(BaseCommand):
    help = 'Print all allowed plan choices for SeatBooking model'

    def handle(self, *args, **options):
        """Print all allowed plan choices"""
        self.stdout.write(self.style.SUCCESS('📋 Allowed Plan Choices for SeatBooking:'))
        self.stdout.write('=' * 50)
        
        choices = dict(SeatBooking.PLAN_CHOICES)
        
        for value, label in choices.items():
            self.stdout.write(f'• {value:15} -> {label}')
        
        self.stdout.write('=' * 50)
        self.stdout.write(self.style.SUCCESS(f'Total choices: {len(choices)}'))
        
        # Show example for frontend
        self.stdout.write('\n📝 Example for Angular frontend:')
        self.stdout.write('plan: "morning_shift"  # NOT "morning"')
        self.stdout.write('plan: "afternoon_shift"')
        self.stdout.write('plan: "evening_shift"')
        self.stdout.write('plan: "full_day"')
        self.stdout.write('plan: "night_shift"')
        self.stdout.write('plan: "24_7_access"')
        self.stdout.write('plan: "hourly"')
        self.stdout.write('plan: "daily"')
        self.stdout.write('plan: "monthly"')

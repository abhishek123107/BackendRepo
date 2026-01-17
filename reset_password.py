import os
import sys
import django

# Add the library_booking_api directory to Python path
sys.path.insert(0, r'c:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking\library_booking_api')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_booking_api.settings')
django.setup()

from accounts.models import User

# Reset admin password
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()
print(f'Password reset for {admin.username}')
print(f'is_staff: {admin.is_staff}, is_superuser: {admin.is_superuser}')

# Create a test student user
student, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student@test.com',
        'first_name': 'Student',
        'last_name': 'User',
        'is_staff': False,
        'is_superuser': False,
    }
)
student.set_password('student123')
student.save()
print(f'\nStudent user: {student.username}')
print(f'Email: {student.email}')
print(f'is_staff: {student.is_staff}, is_superuser: {student.is_superuser}')

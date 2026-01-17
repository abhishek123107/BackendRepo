# Library Seat Booking System - Setup Guide

## Current Status ✅

### Frontend (Angular 18) - RUNNING ON http://localhost:4200

- ✅ Standalone components with lazy loading
- ✅ JWT authentication with refresh tokens
- ✅ Auth guards (AuthGuard, AdminGuard, StudentGuard)
- ✅ HTTP interceptor for token injection and auto-refresh
- ✅ Dark/Light theme toggle with persistence
- ✅ Role-based routing (Student/Admin dashboards)
- ✅ Auth service with login/signup/profile management
- ✅ Responsive UI with Bootstrap 5

### Backend (Django REST API) - READY FOR TESTING

- ✅ Custom User model with membership tracking
- ✅ JWT authentication endpoints
- ✅ Room and Seat management models
- ✅ Booking system with check-in/check-out
- ✅ Membership plans and payment tracking
- ✅ Attendance session management with QR codes
- ✅ All serializers configured

## Backend Setup Instructions

### 1. Activate Virtual Environment

```bash
cd c:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking
backend_env\Scripts\activate
```

### 2. Install/Update Dependencies

```bash
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install pillow qrcode razorpay python-decouple
```

### 3. Run Migrations

```bash
cd library_booking_api
python manage.py makemigrations accounts
python manage.py makemigrations seats
python manage.py makemigrations attendance
python manage.py makemigrations payments
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Email: admin@library.com
# Password: admin123
# First Name: Admin
# Last Name: User
```

### 5. Start Django Development Server

```bash
python manage.py runserver 8000
```

Django will run on: http://localhost:8000

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/login/` - Login with email/phone and password
- `POST /api/auth/register/` - Register new user
- `GET /api/auth/profile/` - Get current user profile (requires auth)
- `PATCH /api/auth/profile/` - Update user profile (requires auth)
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/token/verify/` - Verify token validity

### User Management Endpoints

- `GET /api/accounts/users/` - List all users (admin only)
- `GET /api/accounts/stats/` - Get user statistics (admin only)

### Seats Endpoints

- `GET /api/seats/rooms/` - List all rooms
- `GET /api/seats/seats/` - List all seats
- `POST /api/seats/bookings/` - Create seat booking
- `GET /api/seats/bookings/` - List user's bookings
- `PATCH /api/seats/bookings/{id}/` - Update booking status

### Attendance Endpoints

- `GET /api/attendance/sessions/` - List attendance sessions
- `POST /api/attendance/records/` - Record attendance
- `GET /api/attendance/records/` - Get user attendance records

### Payments Endpoints

- `GET /api/payments/plans/` - List membership plans
- `POST /api/payments/` - Create payment
- `GET /api/payments/` - Get user payments
- `POST /api/payments/{id}/verify/` - Verify offline payment (admin only)

## Frontend Features

### Login/Signup

- Email or phone-based login
- User registration with validation
- Automatic role-based redirect (Student/Admin)
- Remember me functionality via JWT tokens

### Student Dashboard

- Dashboard with welcome message
- Navigation to all student features
- Profile management
- Seat booking with real-time availability
- Attendance tracking
- Payment history
- Notifications
- Feedback submission

### Admin Dashboard

- Seat management and status
- Attendance panel with check-in QR codes
- Payment verification
- Notification broadcasting
- User feedback review
- Leaderboard/statistics

### Theme Toggle

- Dark/Light theme switch
- Persistent theme preference
- CSS variables for easy customization
- Smooth transitions

## Environment Variables

Create a `.env` file in `library_booking_api/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Razorpay (Optional - for payment integration)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Email Settings (Optional - for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@library.com
```

## Testing Endpoints

### Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "admin@library.com",
    "password": "admin123"
  }'
```

### Test Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@library.com",
    "username": "student_user",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+919876543210",
    "student_id": "STU001",
    "department": "Computer Science",
    "year_of_study": 3
  }'
```

## Next Steps to Complete

### 1. Seat Booking Service

- Create seat booking service in Angular
- Implement real-time seat availability
- Add seat preview with photos
- Implement booking form with date/time picker

### 2. Payment Integration

- Implement Razorpay payment gateway
- Add membership plan selection
- Create payment verification workflow
- Add refund handling

### 3. Notifications System

- Create notification service
- Implement real-time notifications (WebSocket)
- Add notification preferences
- Create notification center UI

### 4. Attendance System

- Create QR code scanner component
- Implement attendance check-in/check-out
- Create attendance report views
- Add attendance statistics

### 5. Admin Features

- Implement seat management CRUD
- Create attendance panel with QR codes
- Add payment verification UI
- Create feedback review interface
- Build leaderboard and statistics

### 6. Database Setup

- Consider MongoDB/Djongo setup for better document structure
- Configure database backups
- Set up database indexes for performance

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly (only allow frontend domain)
- [ ] Implement rate limiting
- [ ] Add input validation on all endpoints
- [ ] Set up proper logging and monitoring
- [ ] Configure secure cookies and CSRF protection

## Deployment Ready Components

1. **Frontend:** Ready for Angular build and deployment
2. **Backend:** Ready for gunicorn/wsgi deployment
3. **Database:** Configured for production (use PostgreSQL)
4. **Static Files:** Configure static file serving (use whitenoise or CDN)
5. **Email:** Configure email backend for notifications
6. **Payments:** Configure Razorpay/UPI integration

## Support & Documentation

- Django REST Framework: https://www.django-rest-framework.org/
- Angular Docs: https://angular.io/docs
- Bootstrap Documentation: https://getbootstrap.com/docs
- JWT Documentation: https://tools.ietf.org/html/rfc7519

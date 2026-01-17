# Library Seat Booking System

A full-stack web application for booking library seats with Django backend and Angular frontend.

## Features

- **Seat Management**: View available, booked, and maintenance seats
- **Booking System**: Book seats for different time slots (morning, evening, full-day)
- **Payment Integration**: Support for both online and offline payments
- **File Upload**: Upload payment screenshots for online payments
- **User Authentication**: Secure user management
- **Admin Panel**: Django admin interface for managing seats and bookings
- **Responsive Design**: Bootstrap-based responsive UI

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (can be changed to MySQL/PostgreSQL)
- **Pillow** - Image processing
- **CORS Headers** - Cross-origin resource sharing

### Frontend
- **Angular 18** - Frontend framework
- **Bootstrap 5** - UI components
- **RxJS** - Reactive programming

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate initial seat data:**
   ```bash
   python manage.py populate_seats
   ```

6. **Create superuser (optional for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the backend server:**
   ```bash
   python manage.py runserver 8000
   ```

   Backend will be available at: http://localhost:8000
   Admin panel: http://localhost:8000/admin/

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd LibrarySeatBookig
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   # or
   ng serve
   ```

   Frontend will be available at: http://localhost:4200

## API Endpoints

### Seats
- `GET /api/seats/` - List all seats
- `GET /api/seats/{id}/` - Get specific seat details
- `POST /api/seats/{id}/book/` - Book a specific seat

### Bookings
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/history/` - Get booking history
- `POST /api/bookings/{id}/cancel/` - Cancel a booking

## Database Configuration

### SQLite (Default)
Already configured for development.

### MySQL
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_seat_booking',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### PostgreSQL
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_seat_booking',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Environment Variables

Create a `.env` file in the backend directory:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

## File Structure

```
LibrarySeatBooking/
├── backend/                          # Django backend
│   ├── library_seat_booking/         # Main Django project
│   ├── seats/                        # Seats app
│   ├── db.sqlite3                    # SQLite database
│   ├── manage.py                     # Django management script
│   └── requirements.txt              # Python dependencies
├── LibrarySeatBookig/                # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── services/             # Angular services
│   │   │   ├── models/               # TypeScript interfaces
│   │   │   ├── student/              # Student features
│   │   │   └── ...
│   ├── package.json                  # Node dependencies
│   └── ...
└── README.md                         # This file
```

## Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd LibrarySeatBookig
npm test
```

### Code Formatting
```bash
# Backend (using black)
cd backend
black .

# Frontend (using prettier)
cd LibrarySeatBookig
npx prettier --write .
```

## Deployment

### Backend Deployment
1. Set `DEBUG = False` in settings.py
2. Configure production database
3. Set proper SECRET_KEY
4. Configure static files serving
5. Use a production WSGI server (gunicorn)

### Frontend Deployment
1. Build production bundle: `ng build --prod`
2. Serve static files from `dist/` directory
3. Configure reverse proxy (nginx/apache)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
@echo off
echo Starting Library Seat Booking System...
echo.

echo Setting up backend...
cd backend

echo Installing Python dependencies...
pip install -r requirements.txt

echo Running database migrations...
python manage.py migrate

echo Populating seats data...
python manage.py populate_seats

echo.
echo Starting Django backend server on port 8000...
start cmd /k "python manage.py runserver 8000"

echo.
cd ..

echo Setting up frontend...
cd LibrarySeatBookig

echo Installing Node.js dependencies...
npm install

echo.
echo Starting Angular development server on port 4200...
start cmd /k "npm start"

echo.
echo Servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:4200
echo Admin Panel: http://localhost:8000/admin/
echo.
pause
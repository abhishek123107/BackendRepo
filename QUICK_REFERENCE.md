# 🎯 Library Seat Booking System - Quick Reference Guide

## 🚀 Starting the Application

### Option 1: Use Two Terminal Windows (Recommended)

**Terminal 1 - Angular Frontend:**

```powershell
cd c:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking\LibrarySeatBookig
npm start
```

Expected output:

```
Application bundle generation complete. [3.779 seconds]
➜  Local:   http://localhost:4200/
```

**Terminal 2 - Django Backend:**

```powershell
cd c:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking\library_booking_api
python manage.py runserver 8000
```

Expected output:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Option 2: Use VS Code Terminals

1. Click **Terminal** menu → **New Terminal** (creates Terminal 1)
2. Click the **+** icon in terminal panel (creates Terminal 2)
3. Run one command in each terminal

---

## 🌐 Accessing the Application

### Frontend

- **URL:** http://localhost:4200
- **Features:** Login, Signup, Student Dashboard, Admin Dashboard, Theme Toggle
- **Technology:** Angular 18 + Bootstrap 5

### Backend Admin Interface

- **URL:** http://localhost:8000/admin/
- **Credentials:**
  - Username: `admin`
  - Password: `admin123`
- **Technology:** Django Admin

### API Documentation

- **Base URL:** http://localhost:8000/api/
- **Format:** JSON
- **Authentication:** JWT Bearer Token

---

## 🔑 User Accounts

### Pre-configured Admin Account

```
Email: admin@library.com
Password: admin123
Role: Admin (is_staff=True)
```

### Test Student Account (Create via Signup)

```
Email: student@example.com
Username: studentuser
Password: SecurePass123
Role: Student
```

---

## 🧪 Testing Workflow

### 1. Test Signup

1. Go to http://localhost:4200
2. Click "Sign Up"
3. Fill in the form:
   - Email: `student1@test.com`
   - Username: `student1`
   - Password: `Test@1234`
   - First Name: `John`
   - Last Name: `Doe`
4. Click "Sign Up"
5. Should redirect to Student Dashboard

### 2. Test Login

1. Go to http://localhost:4200
2. Click "Login"
3. Enter email: `student1@test.com`
4. Enter password: `Test@1234`
5. Click "Login"
6. Should redirect to Student Dashboard

### 3. Test Theme Toggle

1. Look at top-right corner of navbar
2. Click the theme toggle icon
3. Page should switch to dark mode
4. Click again to switch back to light
5. Refresh page - theme should persist

### 4. Test Admin Access

1. Login as admin: `admin@library.com` / `admin123`
2. Should redirect to Admin Dashboard
3. Try accessing `/student` route
4. Should redirect back to admin dashboard

### 5. Test Auth Guard

1. Logout by clicking logout button
2. Try accessing http://localhost:4200/student
3. Should redirect to login page

---

## 📱 Component Hierarchy

```
AppComponent
├── Router Outlet
│   ├── HomeComponent (/)
│   ├── LoginComponent (/login)
│   ├── SignupComponent (/signup)
│   ├── StudentDashboardComponent (/student)
│   │   ├── NavbarComponent
│   │   ├── Router Outlet (children)
│   │   │   ├── SeatBookingComponent
│   │   │   ├── AttendanceComponent
│   │   │   ├── PaymentsComponent
│   │   │   ├── NotificationsComponent
│   │   │   └── ProfileComponent
│   │   └── ThemeToggleComponent
│   └── AdminDashboardComponent (/admin)
│       ├── NavbarComponent
│       ├── Router Outlet (children)
│       │   ├── SeatManagementComponent
│       │   ├── AttendancePanelComponent
│       │   ├── PaymentVerificationComponent
│       │   ├── NotificationsSenderComponent
│       │   ├── FeedbackComponent
│       │   └── LeaderboardComponent
│       └── ThemeToggleComponent
```

---

## 🔄 API Flow Examples

### Login Flow

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "admin@library.com",
    "password": "admin123"
  }'
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@library.com",
    "username": "admin",
    "is_staff": true,
    "is_superuser": true,
    ...
  }
}
```

### Get Profile (Authenticated)

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## 🛠️ Troubleshooting

### Issue: "Port 4200 is already in use"

**Solution:** Kill existing process

```powershell
Get-Process node | Stop-Process -Force
npm start
```

### Issue: "Port 8000 is already in use"

**Solution:** Use different port

```powershell
python manage.py runserver 8001
```

### Issue: "Cannot POST /api/auth/login/"

**Possible causes:**

- Django server not running
- Check backend URL in auth.service.ts
- CORS not configured properly

**Solution:**

```
1. Verify Django running: http://localhost:8000/admin/
2. Check console errors in browser (F12)
3. Check Django terminal for errors
```

### Issue: "CORS error when calling API"

**Solution:** Update CORS in settings.py

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
```

### Issue: "TypeError: Cannot read property 'isAdmin' of null"

**Solution:** AuthService not loaded yet

- This is normal during initialization
- Guards prevent access before auth service loads
- Check console to verify

---

## 📊 Directory Structure Quick Reference

```
LibrarySeatBooking/
├── LibrarySeatBookig/           ← Angular Frontend (Port 4200)
│   ├── src/app/
│   │   ├── auth/                ← Login/Signup
│   │   ├── student/             ← Student Features
│   │   ├── admin/               ← Admin Features
│   │   ├── services/            ← Angular Services
│   │   ├── guards/              ← Route Guards
│   │   ├── interceptors/        ← HTTP Interceptors
│   │   └── shared/              ← Shared Components
│   ├── package.json
│   └── angular.json
│
├── library_booking_api/         ← Django Backend (Port 8000)
│   ├── accounts/                ← User Auth
│   ├── seats/                   ← Seat Booking
│   ├── attendance/              ← Attendance
│   ├── payments/                ← Payments
│   ├── manage.py
│   └── db.sqlite3               ← Database
│
├── backend_env/                 ← Python Virtual Environment
├── README.md                    ← Full Documentation
├── SETUP_GUIDE.md              ← Setup Instructions
└── IMPLEMENTATION_SUMMARY.md   ← Implementation Details
```

---

## 🔐 Authentication Flow Diagram

```
┌─────────────────────┐
│   User Login Page   │
└──────────┬──────────┘
           │ User enters credentials
           ▼
┌─────────────────────────┐
│ POST /api/auth/login/   │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────┐
│ Backend Validates    │
│ Credentials          │
└──────────┬───────────┘
           │
    ┌──────┴──────┐
    │             │
   YES            NO
    │             │
    ▼             ▼
┌─────────────┐ ┌──────────────┐
│ Generate    │ │ Return Error │
│ JWT Tokens  │ │ 400/401      │
└──────┬──────┘ └──────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Return {access, refresh,    │
│ user} to Frontend           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Frontend Stores Tokens in   │
│ LocalStorage                │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ AuthService Notifies        │
│ Subscribers (Guards, etc)   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Router Redirects Based on   │
│ Role (Student/Admin)        │
└─────────────────────────────┘
```

---

## 🎨 Theme System

### Available Themes

- **Light Mode** (Default) - Clean white interface
- **Dark Mode** - Dark interface for reduced eye strain

### Theme Colors

#### Light Theme

```css
--bg-primary: #ffffff
--bg-secondary: #f5f5f5
--text-primary: #212121
--accent-color: #007bff
```

#### Dark Theme

```css
--bg-primary: #121212
--bg-secondary: #1e1e1e
--text-primary: #ffffff
--accent-color: #4a9eff
```

### Toggle Theme

Click the circle/sun icon in the top-right navbar to toggle themes.

---

## 📈 Performance Tips

### Frontend Optimization

- ✅ Already using tree-shaking via standalone components
- ✅ Angular CLI optimization enabled
- ✅ CSS variables for instant theme switching

### Backend Optimization

- ✅ JWT tokens reduce database queries
- ✅ Token caching in localStorage
- ✅ Efficient serializer validation

### Browser Caching

- ✅ LocalStorage for tokens (faster than session)
- ✅ Theme preference persistent
- ✅ Static files cached

---

## 🆘 Getting Help

### Check Logs

**Browser Console (F12):**

- JavaScript errors
- Network requests/responses
- Console.log debug messages

**Django Terminal:**

- Server startup messages
- Request handling logs
- SQL queries (if DEBUG=True)

### Common Error Messages

| Error                          | Cause                      | Solution                           |
| ------------------------------ | -------------------------- | ---------------------------------- |
| `Cannot POST /api/auth/login/` | Django not running         | Start Django server                |
| `CORS error`                   | CORS not configured        | Check CORS_ALLOWED_ORIGINS         |
| `401 Unauthorized`             | Invalid token              | Re-login                           |
| `Cannot find module`           | Missing dependency         | Run `npm install` or `pip install` |
| `Port already in use`          | Another process using port | Kill process and restart           |

---

## 📚 File Locations

| Component         | File Location                                               |
| ----------------- | ----------------------------------------------------------- |
| Login Form        | `LibrarySeatBookig/src/app/auth/login/`                     |
| Signup Form       | `LibrarySeatBookig/src/app/auth/signup/`                    |
| Auth Service      | `LibrarySeatBookig/src/app/services/auth.service.ts`        |
| Auth Guard        | `LibrarySeatBookig/src/app/guards/auth.guard.ts`            |
| JWT Interceptor   | `LibrarySeatBookig/src/app/interceptors/jwt.interceptor.ts` |
| Theme Service     | `LibrarySeatBookig/src/app/services/theme.service.ts`       |
| Global Styles     | `LibrarySeatBookig/src/styles.css`                          |
| Django Auth Views | `library_booking_api/accounts/views.py`                     |
| Django User Model | `library_booking_api/accounts/models.py`                    |
| Django Settings   | `library_booking_api/library_booking_api/settings.py`       |
| Django URLs       | `library_booking_api/library_booking_api/urls.py`           |

---

## ✅ Verification Checklist

After starting the application, verify:

- [ ] Angular frontend loads at http://localhost:4200
- [ ] Django backend responds at http://localhost:8000/admin/
- [ ] Login page displays without errors
- [ ] Can signup with new user account
- [ ] Can login with credentials
- [ ] Dashboard loads after login
- [ ] Theme toggle works (switch between light/dark)
- [ ] Logout button works
- [ ] Accessing `/student` while logged out redirects to login
- [ ] Admin user redirects to admin dashboard
- [ ] Student user redirects to student dashboard

---

## 🎓 Next Development Steps

### Frontend Features to Build

1. [ ] Seat Booking UI and form
2. [ ] Real-time availability display
3. [ ] Payment interface
4. [ ] Attendance tracking
5. [ ] Notification center

### Backend Features to Build

1. [ ] Seat booking endpoints
2. [ ] Seat availability checking
3. [ ] Payment processing
4. [ ] Attendance recording
5. [ ] Notification system

### Database/DevOps

1. [ ] MongoDB/Postgres setup
2. [ ] Database backup strategy
3. [ ] Environment-specific configs
4. [ ] Deployment pipeline
5. [ ] Monitoring and logging

---

**Last Updated:** January 9, 2026
**Status:** Ready for Development ✅
**Next Phase:** Feature Implementation

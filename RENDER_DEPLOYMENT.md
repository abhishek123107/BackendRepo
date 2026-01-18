# Render Django Deployment Guide

## 1. Setup Render Account
- Go to [render.com](https://render.com)
- Sign up/login with GitHub
- Create new "Web Service"

## 2. Repository Settings
- Connect your GitHub repository
- Branch: `main`
- Root Directory: `BackendPanel`
- Runtime: `Python 3`

## 3. Build Settings
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `gunicorn backend.library_seat_booking.wsgi:application`

## 4. Environment Variables
Copy from `.env.render` file:
```
DJANGO_SETTINGS_MODULE=library_seat_booking.production_settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-app-name.onrender.com
DATABASE_URL=postgresql://username:password@host:port/database_name
```

## 5. Database Setup
- Render automatically creates PostgreSQL database
- Copy DATABASE_URL from Render dashboard
- Add to environment variables

## 6. Deploy
- Click "Create Web Service"
- Render will auto-deploy from GitHub
- Your app will be available at: `https://your-app-name.onrender.com`

## 7. Update Frontend
Change `environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-app-name.onrender.com/api',
  backendUrl: 'https://your-app-name.onrender.com'
};
```

## 8. Test Endpoints
- GET: `https://your-app-name.onrender.com/api/seats/`
- POST: `https://your-app-name.onrender.com/api/accounts/login/`
- Admin: `https://your-app-name.onrender.com/admin/`

## Advantages over Vercel
✅ Native Django support
✅ Built-in PostgreSQL database
✅ Proper WSGI deployment
✅ No function size limits
✅ Better logging and monitoring

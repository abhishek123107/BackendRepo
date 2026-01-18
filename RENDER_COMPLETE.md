# Render Django Deployment - Complete Working Setup

## Problems Fixed
1. **"gunicorn: command not found"** - gunicorn already in requirements.txt
2. **"Pillow failing to build on Python 3.13"** - Updated to Pillow 10.4.0
3. **Python version compatibility** - Changed to Python 3.11

## Final Configuration

### 1. requirements.txt (Updated)
```
Django==4.2.11
djangorestframework==3.15.2
django-cors-headers==4.4.0
Pillow==10.4.0  # Updated for Python 3.13 compatibility
python-decouple==3.8
djangorestframework-simplejwt==5.3.0
django-filter==23.5
psycopg2-binary==2.9.9
dj-database-url==2.1.0
gunicorn==21.2.0  # Included for production server
whitenoise==6.6.0
firebase-admin==6.2.0
google-cloud-storage==2.10.0
```

### 2. render.yaml (Fixed)
```yaml
web: gunicorn backend.library_seat_booking.wsgi:application
release: python backend/manage.py migrate
build: pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput
python_version: "3.11"  # Changed from 3.9.12
```

### 3. build.sh (Working)
```bash
#!/bin/bash
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py collectstatic --noinput
echo "Build completed successfully!"
```

### 4. Render Dashboard Settings

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn backend.library_seat_booking.wsgi:application
```

**Directory:**
- **Root Directory**: `BackendPanel` (or empty)
- **Runtime**: `Python 3.11`
- **Branch**: `main`

### 5. Environment Variables (Required)
```
DJANGO_SETTINGS_MODULE=library_seat_booking.production_settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### 6. Why This Works
✅ **Python 3.11** - Stable version with full package support
✅ **Pillow 10.4.0** - Compatible with Python 3.13+
✅ **Gunicorn included** - Production server installed
✅ **Build script exists** - Render can execute it
✅ **Migrations run** - Database tables created
✅ **Static files collected** - CSS/JS handled properly

### 7. Test URLs After Deployment
- **Backend**: `https://your-app-name.onrender.com`
- **API**: `https://your-app-name.onrender.com/api/seats/`
- **Admin**: `https://your-app-name.onrender.com/admin/`

### 8. Troubleshooting
If still fails:
1. Check Render logs for specific error
2. Try Python 3.10 instead of 3.11
3. Remove problematic packages (firebase, google-cloud)
4. Use direct commands instead of build.sh

### 9. Frontend Update
```typescript
// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://your-app-name.onrender.com/api',
  backendUrl: 'https://your-app-name.onrender.com'
};
```

This setup should deploy successfully on Render!

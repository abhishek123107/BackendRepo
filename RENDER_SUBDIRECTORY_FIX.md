# Render Django Deployment - Subdirectory Fix

## Problems Identified
1. **"ModuleNotFoundError: No module named 'library_seat_booking'"** - Django can't find project
2. **"pkg_resources not found"** - setuptools/setuptools issue
3. **Subdirectory structure** - Django project in backend/library_seat_booking

## Solution - Correct Configuration

### 1. render.yaml (Fixed for subdirectory)
```yaml
web: gunicorn backend.library_seat_booking.wsgi:application
release: cd backend && python manage.py migrate
build: pip install -r backend/requirements.txt && cd backend && python manage.py collectstatic --noinput
python_version: "3.11"
```

### 2. build.sh (Fixed for subdirectory)
```bash
#!/bin/bash
pip install -r backend/requirements.txt
cd backend && python manage.py migrate
cd backend && python manage.py collectstatic --noinput
echo "Build completed successfully!"
```

### 3. requirements.txt (Updated for compatibility)
```
Django==4.2.11
djangorestframework==3.15.2
django-cors-headers==4.4.0
Pillow==10.4.0
python-decouple==3.8
djangorestframework-simplejwt==5.3.0
django-filter==23.5
psycopg2-binary==2.9.9
dj-database-url==2.1.0
gunicorn==21.2.0
whitenoise==6.6.0
firebase-admin==6.2.0
google-cloud-storage==2.10.0
setuptools==65.5.0  # Fix pkg_resources issue
```

### 4. Render Dashboard Settings

**Root Directory**: `BackendPanel` (leave empty if repo root)
**Runtime**: `Python 3.11`
**Branch**: `main`

**Build Command**: `./build.sh`

**Start Command**: `gunicorn backend.library_seat_booking.wsgi:application`

### 5. Environment Variables
```
DJANGO_SETTINGS_MODULE=library_seat_booking.production_settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### 6. Project Structure
```
BackendPanel/
├── backend/
│   ├── library_seat_booking/  # Django project
│   ├── manage.py
│   └── requirements.txt
├── build.sh
└── render.yaml
```

### 7. Why This Works
✅ **cd backend** - All Django commands run from correct directory
✅ **setuptools** - Fixes pkg_resources error
✅ **Python 3.11** - Stable version with full support
✅ **Correct WSGI path** - Points to backend.library_seat_booking.wsgi
✅ **Proper migrations** - Database tables created correctly

### 8. Test URLs
- **Backend**: `https://your-app-name.onrender.com`
- **API**: `https://your-app-name.onrender.com/api/seats/`
- **Admin**: `https://your-app-name.onrender.com/admin/`

### 9. Troubleshooting
If still fails:
1. Check Render logs for exact error
2. Try Python 3.10 instead of 3.11
3. Remove optional packages (firebase, google-cloud)
4. Use absolute paths in build.sh

This should fix the module not found and pkg_resources errors!

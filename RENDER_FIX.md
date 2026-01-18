# Render Django Deployment - Complete Setup

## Problem Analysis
Error: "bash: line 1: ./build.sh: No such file or directory"
- Render was looking for build.sh but it didn't exist
- Need proper build script and configuration

## Solution

### 1. build.sh (Created)
```bash
#!/bin/bash
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py collectstatic --noinput
echo "Build completed successfully!"
```

### 2. render.yaml (Updated)
```yaml
web: gunicorn backend.library_seat_booking.wsgi:application
release: python backend/manage.py migrate
build: pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput
python_version: "3.9.12"
```

### 3. Render Dashboard Settings

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn backend.library_seat_booking.wsgi:application
```

**Directory Setup:**
- **Root Directory**: `BackendPanel` (or leave empty if repo root)
- **Runtime**: `Python 3`
- **Branch**: `main`

### 4. Environment Variables (Required)
```
DJANGO_SETTINGS_MODULE=library_seat_booking.production_settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### 5. Why This Works
✅ **build.sh exists** - Render can find and execute it
✅ **Dependencies installed** - pip installs from requirements.txt
✅ **Database migrations** - Django tables created automatically
✅ **Static files collected** - CSS/JS properly handled
✅ **Gunicorn WSGI** - Production-ready server

### 6. Alternative (Simpler) Setup
If build.sh still causes issues, use direct commands:

**Build Command:**
```
pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn backend.library_seat_booking.wsgi:application
```

### 7. Test After Deployment
- API: `https://your-app-name.onrender.com/api/seats/`
- Admin: `https://your-app-name.onrender.com/admin/`
- Health: `https://your-app-name.onrender.com/`

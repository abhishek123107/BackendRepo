# Render Environment Variables Setup Guide

## 🚀 **Required Environment Variables for Render**

### **1. Basic Django Settings**
```
NAME_OF_VARIABLE: VALUE
```

**Required Variables:**
```
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=backendrepo-5.onrender.com,*.onrender.com
```

### **2. Database Configuration**
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Steps:**
1. Go to Render Dashboard → Your Service → Environment
2. Add PostgreSQL database (if not already added)
3. Copy Database URL from Render database settings
4. Paste as DATABASE_URL environment variable

### **3. CORS Settings**
```
CORS_ALLOWED_ORIGINS=https://front-repo-liard.vercel.app,https://backendrepo-5.onrender.com,https://*.onrender.com
CORS_ALLOW_ALL_ORIGINS=False
```

### **4. Security Settings**
```
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### **5. JWT Settings**
```
JWT_SECRET_KEY=your-jwt-secret-key-different-from-django-secret
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=10080
```

## 🔧 **Setup Steps**

### **Step 1: Render Dashboard**
1. Go to https://dashboard.render.com
2. Select your backend service
3. Go to "Environment" tab

### **Step 2: Add Environment Variables**
Add these variables in Render dashboard:

```
DEBUG=False
DJANGO_SETTINGS_MODULE=library_booking_api.settings
SECRET_KEY=django-insecure-iv*g$pfm_@j5-gutyl@m8^vna)z60th=-_^uv!odz&&o3az#=r
ALLOWED_HOSTS=backendrepo-5.onrender.com,*.onrender.com
CORS_ALLOWED_ORIGINS=https://front-repo-liard.vercel.app,https://backendrepo-5.onrender.com,https://*.onrender.com
CORS_ALLOW_ALL_ORIGINS=False
JWT_SECRET_KEY=jwt-secret-key-for-library-seat-booking-app
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=10080
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### **Step 3: Database Setup**
1. If using PostgreSQL, add database in Render
2. Copy the connection string
3. Add as `DATABASE_URL` environment variable

### **Step 4: Deploy**
1. Push changes to GitHub
2. Render will auto-deploy
3. Monitor build logs

## 🌐 **Expected URLs After Setup**

- **Root**: https://backendrepo-5.onrender.com/ (Shows server status)
- **Admin**: https://backendrepo-5.onrender.com/admin/
- **API**: https://backendrepo-5.onrender.com/api/
- **Auth**: https://backendrepo-5.onrender.com/api/auth/token/

## ✅ **Verification**

After deployment, test these URLs:
1. **Root URL**: Should show JSON response with server status
2. **Admin Panel**: Should load Django admin
3. **API Endpoints**: Should be accessible from frontend
4. **CORS**: Should allow frontend domain

## 🚨 **Troubleshooting**

**If 404 errors:**
- Check ALLOWED_HOSTS includes your Render domain
- Verify DJANGO_SETTINGS_MODULE is correct

**If CORS errors:**
- Verify CORS_ALLOWED_ORIGINS includes frontend domain
- Check CORS_ALLOW_ALL_ORIGINS is False in production

**If database errors:**
- Verify DATABASE_URL is correct
- Check database is running in Render

## 🔄 **Local Testing**

To test production settings locally:
```bash
# Set environment variables
export DEBUG=False
export ALLOWED_HOSTS=localhost,127.0.0.1
export CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200

# Run server
python manage.py runserver 0.0.0.0:8000
```

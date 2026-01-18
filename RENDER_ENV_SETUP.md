# Render Environment Variables Setup

## Step 1: Render Dashboard Environment Variables

Go to Render dashboard → Your Project → Environment → Add Environment Variable

### Required Environment Variables:

**1. DJANGO_ALLOWED_HOSTS (NEW)**
```
Name: DJANGO_ALLOWED_HOSTS
Value: backendrepo-5.onrender.com
```

**2. Other Required Variables:**
```
Name: DJANGO_SETTINGS_MODULE
Value: library_seat_booking.production_settings

Name: SECRET_KEY
Value: your-secret-key-here

Name: DEBUG
Value: False

Name: CORS_ALLOWED_ORIGINS
Value: https://your-frontend-url.vercel.app,https://backendrepo-5.onrender.com

Name: DATABASE_URL
Value: postgresql://user:pass@host:port/dbname
```

## Step 2: Updated production_settings.py

The settings now support DJANGO_ALLOWED_HOSTS with priority:

```python
# Allowed hosts for production
# Priority: DJANGO_ALLOWED_HOSTS env var > ALLOWED_HOSTS env var > default
django_allowed_hosts = config('DJANGO_ALLOWED_HOSTS', default='')
if django_allowed_hosts:
    ALLOWED_HOSTS = django_allowed_hosts.split(',')
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*.vercel.app,localhost,127.0.0.1', cast=Csv())
```

## Step 3: How It Works

1. **DJANGO_ALLOWED_HOSTS** has highest priority
2. If set, it overrides all other ALLOWED_HOSTS settings
3. If not set, falls back to ALLOWED_HOSTS env var
4. If neither set, uses default values

## Step 4: Benefits

✅ **Automatic**: No manual code changes needed
✅ **Flexible**: Support multiple hosts (comma-separated)
✅ **Safe**: Fallback to defaults if env var missing
✅ **Deploy-friendly**: Works across different environments

## Step 5: Example Values

**Single Host:**
```
DJANGO_ALLOWED_HOSTS=backendrepo-5.onrender.com
```

**Multiple Hosts:**
```
DJANGO_ALLOWED_HOSTS=backendrepo-5.onrender.com,localhost,127.0.0.1
```

## Step 6: Testing

After setting environment variables:
1. Redeploy on Render
2. Check that your domain works without ALLOWED_HOSTS errors
3. Verify Django admin panel loads correctly

This approach makes deployment completely automatic!

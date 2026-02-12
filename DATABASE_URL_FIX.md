# DATABASE_URL Configuration Guide for Render

## 🔧 **Correct DATABASE_URL Format for PostgreSQL**

### **Render PostgreSQL Format:**
```
postgresql://username:password@host:port/database_name
```

### **Example:**
```
postgresql://myuser:mypassword@mydatabase.abc123.rds.amazonaws.com:5432/mydatabase
```

---

## 🚀 **How to Get DATABASE_URL from Render**

### **Step 1: Find Your Database in Render**
1. Go to Render Dashboard
2. Click on your PostgreSQL database
3. Go to "Connections" tab
4. Copy the "External Database URL"

### **Step 2: Format for Environment Variable**
The URL will look like:
```
postgresql://your_username:your_password@your_host:5432/your_database_name
```

---

## 🔧 **Render Environment Variable Setup**

### **Method 1: Use Render's Built-in DATABASE_URL**
1. In your web service settings
2. Go to "Environment" tab
3. Add your PostgreSQL database as a dependency
4. Render automatically provides `DATABASE_URL`

### **Method 2: Manual Configuration**
1. Copy the External Database URL from your database service
2. In your web service → Environment → Add Environment Variable
3. Set:
   - **Name**: `DATABASE_URL`
   - **Value**: `postgresql://username:password@host:5432/database_name`

---

## 🛡️ **Safer Database Configuration**

### **Using dj_database_url.config()**
```python
import dj_database_url
from decouple import config

# Safe database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

### **Benefits:**
- ✅ **Auto-parsing**: Handles URL parsing automatically
- ✅ **Fallback**: Uses SQLite if DATABASE_URL is missing
- ✅ **Connection pooling**: Reuses database connections
- ✅ **Health checks**: Monitors connection health

---

## 🐛 **Common DATABASE_URL Errors**

### **Error 1: "Port could not be cast to integer"**
**Cause**: Port contains non-numeric characters
**Solution**: Ensure port is a number (usually 5432)

### **Error 2: "Invalid DATABASE_URL format"**
**Cause**: URL syntax is incorrect
**Solution**: Use proper format: `postgresql://user:pass@host:port/db`

### **Error 3: "Connection refused"**
**Cause**: Database is not accessible
**Solution**: Check firewall and connection settings

---

## 🔍 **Debugging DATABASE_URL**

### **Add Debug Code to settings.py:**
```python
import dj_database_url
from decouple import config

# Debug DATABASE_URL
database_url = config('DATABASE_URL', default='')
print(f"DATABASE_URL: {database_url}")

if database_url:
    try:
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        print("Database configured successfully")
    except Exception as e:
        print(f"Database configuration error: {e}")
        # Fallback to SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    print("No DATABASE_URL found, using SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

---

## 🔄 **How to Redeploy After Fixing**

### **Step 1: Update Environment Variables**
1. Go to Render Dashboard → Your Service
2. Go to "Environment" tab
3. Update or add `DATABASE_URL`
4. Save changes

### **Step 2: Trigger Redeploy**
1. Go to "Events" tab in your service
2. Click "Manual Deploy" → "Deploy Latest Commit"
3. Or push a new commit to trigger auto-deploy

### **Step 3: Monitor Build Logs**
1. Watch the build process
2. Check for database connection errors
3. Verify migrations run successfully

---

## 📱 **Testing Database Connection**

### **After Deployment:**
1. Visit: `https://your-app.onrender.com/`
2. Should show server status JSON
3. Check logs for database connection messages

### **Manual Test:**
```python
# In Django shell
python manage.py shell

# Test database connection
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
result = cursor.fetchone()
print(f"Database connection test: {result}")
```

---

## 🎯 **Production Ready Configuration**

### **Final settings.py database section:**
```python
import dj_database_url
from decouple import config

# Production database configuration
if config('DATABASE_URL', default=''):
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

This configuration:
- ✅ **Works in production** (uses DATABASE_URL)
- ✅ **Works in development** (falls back to SQLite)
- ✅ **Handles errors gracefully**
- ✅ **Provides connection pooling**
- ✅ **Includes health checks**

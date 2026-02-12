"""
Production settings for library_booking_api project.
This file is used when DEBUG=False
"""

from .settings import *
import os

# Production-specific settings
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_FRAME_DENY = True

# Session settings for production
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Database configuration (use Render's PostgreSQL)
import dj_database_url
from decouple import config

# Debug: Print the raw DATABASE_URL to see what's wrong
raw_database_url = config('DATABASE_URL', default='')
print(f"🔍 RAW DATABASE_URL: '{raw_database_url}'")
print(f"🔍 DATABASE_URL length: {len(raw_database_url)}")
if raw_database_url:
    print(f"🔍 First 50 chars: {raw_database_url[:50]}")
    print(f"🔍 Last 50 chars: {raw_database_url[-50:]}")
else:
    print("🔍 DATABASE_URL is empty")

# Parse DATABASE_URL with proper error handling and fallback
try:
    database_url = config('DATABASE_URL', default='')
    
    if database_url and database_url.startswith('postgresql://'):
        # Additional validation
        if ':port/' in database_url:
            print("❌ ERROR: DATABASE_URL contains literal 'port' instead of port number")
            print("❌ Please fix DATABASE_URL in Render dashboard")
            raise ValueError("DATABASE_URL contains literal 'port' - must be numeric port like 5432")
        
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=True,  # Required for Render PostgreSQL
            )
        }
        print("✅ PostgreSQL database configured successfully")
    else:
        # Fallback to SQLite for local development
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        print("⚠️  Using SQLite fallback (no valid DATABASE_URL)")
        
except Exception as e:
    print(f"❌ Database configuration error: {e}")
    print("🔄 Falling back to SQLite")
    print("🔧 TO FIX: Update DATABASE_URL in Render dashboard with correct format")
    print("🔧 Format: postgresql://username:password@host:5432/database_name")
    # Safe fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files configuration for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

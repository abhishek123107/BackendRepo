import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_seat_booking.production_settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()

# Vercel serverless function handler
def handler(event, context):
    # Convert Vercel event to WSGI environ
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', 'application/json'),
        'CONTENT_LENGTH': str(len(event.get('body', ''))),
        'SERVER_NAME': 'vercel.app',
        'SERVER_PORT': '443',
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in event.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Call Django application
    response = application(environ, lambda status, headers: None)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': 'Django app is running'
    }

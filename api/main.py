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
def handler(request):
    # Convert Vercel request to WSGI environ
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    headers = request.get('headers', {})
    query_string = request.get('query', '')
    body = request.get('body', '')
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', 'application/json'),
        'CONTENT_LENGTH': str(len(body) if body else '0'),
        'SERVER_NAME': 'vercel.app',
        'SERVER_PORT': '443',
        'wsgi.url_scheme': 'https',
        'wsgi.input': body,
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Call Django application
    response_data = {}
    def start_response(status, response_headers):
        response_data['status'] = status
        response_data['headers'] = response_headers
    
    # Get response from Django
    response_body = application(environ, start_response)
    
    # Convert to Vercel format
    status_code = int(response_data['status'].split()[0])
    response_headers = dict(response_data['headers'])
    response_body_text = ''.join(chunk.decode() if isinstance(chunk, bytes) else chunk for chunk in response_body)
    
    return {
        'statusCode': status_code,
        'headers': response_headers,
        'body': response_body_text
    }

# Export the handler for Vercel
__all__ = ['handler']

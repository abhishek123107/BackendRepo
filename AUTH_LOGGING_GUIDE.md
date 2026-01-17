# Auth Endpoints - Logging & Error Handling Summary

## Changes Made

### 1. Added Structured Error Responses

- Login and register endpoints now return **JSON validation errors** when requests fail
- Errors include field-level details (e.g., "Email is required", "Passwords do not match")
- All 400 errors return structured JSON responses (no more empty bodies)

### 2. Added Multiple Parser Support

- Both `/api/auth/login/` and `/api/auth/register/` accept:
  - **application/json** (JSON POST bodies)
  - **application/x-www-form-urlencoded** (form-encoded)
  - **multipart/form-data** (file uploads, form fields)

### 3. Implemented Comprehensive Logging

- Created `logs/` directory with two log files:

  - **logs/auth.log** — Captures all authentication/registration events
  - **logs/django.log** — Captures all Django INFO+ events

- Log entries include:
  - ✅ Successful logins: `User {username} logged in successfully`
  - ✅ New registrations: `New user registered: {username} ({email})`
  - ⚠️ Validation failures: Login/registration errors with field details
  - ⚠️ Empty request bodies: `Registration attempt with empty request body`
  - 🔴 Server errors: Exception stack traces

### 4. Cleaned Serializers

- Removed duplicate class definitions in `accounts/serializers.py`
- Enhanced field-level validation with clear error messages
- Added extra_kwargs for username and email required constraints

## Log File Locations

```
library_booking_api/
  logs/
    auth.log       # Authentication & registration logs
    django.log     # General Django logs
    .gitkeep
```

## Example Log Entries

### Success

```
INFO 2026-01-09 19:15:14,018 accounts.views User admin logged in successfully
INFO 2026-01-09 19:15:01,128 accounts.views New user registered: gooduser20260109191500 (gooduser20260109191500@library.com)
```

### Validation Failures

```
WARNING 2026-01-09 19:15:14,509 accounts.views Login validation failed: {'non_field_errors': [ErrorDetail(string='Invalid credentials', code='invalid')]}
WARNING 2026-01-09 19:14:32,522 accounts.views Registration validation failed: {'username': [ErrorDetail(string='A user with that username already exists.', code='unique')], 'password_confirm': [ErrorDetail(string='Password confirmation is required', code='required')]}
```

## Testing the Endpoints

### Valid Registration (JSON)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@library.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Invalid Registration (Missing Email)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

Response:

```json
{
  "email": ["Email is required"],
  "password_confirm": ["This field may not be blank."]
}
```

### Valid Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "admin@library.com",
    "password": "admin123"
  }'
```

Response includes tokens and user data (201 status).

### Invalid Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "wrong@library.com",
    "password": "wrongpass"
  }'
```

Response:

```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

## Debugging

To monitor auth logs in real-time:

```bash
# Windows PowerShell
Get-Content library_booking_api/logs/auth.log -Wait

# Or view last N entries
Get-Content library_booking_api/logs/auth.log | Select-Object -Last 20
```

## Files Modified

1. **accounts/views.py**

   - Added `logging` import and logger setup
   - Enhanced login/register with logging calls
   - Added parser classes for multiple content types

2. **accounts/serializers.py**

   - Removed duplicate class definitions
   - Maintained robust field-level validation

3. **library_booking_api/settings.py**

   - Added LOGGING configuration
   - Configured file handlers for auth.log and django.log
   - Set log level to DEBUG for auth app, INFO for Django

4. **logs/** (new directory)
   - Created logs directory with .gitkeep

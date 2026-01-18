#!/bin/bash

# Install Python dependencies
pip install -r backend/requirements.txt

# Run Django migrations
cd backend && python manage.py migrate

# Collect static files
cd backend && python manage.py collectstatic --noinput

echo "Build completed successfully!"

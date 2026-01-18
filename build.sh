#!/bin/bash

# Install Python dependencies
pip install -r backend/requirements.txt

# Run Django migrations
python backend/manage.py migrate

# Collect static files
python backend/manage.py collectstatic --noinput

echo "Build completed successfully!"

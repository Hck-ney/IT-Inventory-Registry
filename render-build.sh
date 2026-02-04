#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files (CSS/JS) for production
python manage.py collectstatic --no-input

# Apply database changes
python manage.py migrate

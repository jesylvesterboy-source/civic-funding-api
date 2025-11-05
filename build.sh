#!/usr/bin/env bash
set -o errexit

echo "=== PROFESSIONAL ENTERPRISE DEPLOYMENT ==="

echo "1. Installing system dependencies..."
apt-get update
apt-get install -y libpq-dev gcc python3-dev

echo "2. Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "3. Running database migrations..."
python manage.py migrate

echo "4. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo " PROFESSIONAL DEPLOYMENT COMPLETED SUCCESSFULLY"

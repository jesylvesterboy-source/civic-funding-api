#!/usr/bin/env bash
set -o errexit

echo "=== PROFESSIONAL ENTERPRISE DEPLOYMENT ==="

echo "1. Installing Python dependencies with build isolation..."
pip install --upgrade pip
pip install --no-binary psycopg2 psycopg2==2.9.9
pip install -r requirements.txt

echo "2. Running database migrations..."
python manage.py migrate

echo "3. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo " PROFESSIONAL DEPLOYMENT COMPLETED SUCCESSFULLY"

#!/bin/bash

cd /opt/mysite || exit

echo "Pulling latest code..."
git pull

echo "Activating virtualenv..."
source /opt/mysite/venv/bin/activate

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Deployment finished!"

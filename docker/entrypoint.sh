#!/bin/bash


echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Checking if superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@admin.com').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin');
    print('Superuser created');
else:
    print('Superuser already exists');
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
#!/bin/sh

# need to wait for postgres to be ready
/wait-for-it.sh db:5432 --timeout=60 --strict

# prepare application
python manage.py migrate
python manage.py collectstatic --noinput

#exec gunicorn backend_cloud_dipl.wsgi:application --bind 0.0.0.0:8000
# for server need this option: (for VM Reg Ru)
exec gunicorn backend_cloud_dipl.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300
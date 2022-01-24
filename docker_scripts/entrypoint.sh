#!/bin/bash

# Pick up any local changes to requirements.txt, which do *not* automatically get re-installed when starting the container.
# Do this only in dev environment!
if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  pip install --no-cache-dir -r requirements.txt --user --no-warn-script-location
fi

# Check when database is ready for connections
# Tried script from https://github.com/vishnubob/wait-for-it
# but it's not reliable for Oracle; listener may be up but db not ready.
# Logs will show error until database is ready, which is OK.
until python -c "import os ; import cx_Oracle ; conn = cx_Oracle.connect(os.environ.get('DJANGO_DB_USER'), os.environ.get('DJANGO_DB_PASS'), os.environ.get('DJANGO_DB_DSN'))" ; do
  echo "Database connection not ready - waiting"
  sleep 10
done

if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  # Make sure database migrations are up to date
  python ./manage.py migrate

  # Create default superuser for dev environment, using django env vars.
  # Logs will show error if this exists, which is OK.
  python ./manage.py createsuperuser --no-input
fi

# Django app server is fine for development
if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  python ./manage.py runserver 0.0.0.0:8000
#else
  # Start the production app server
  #gunicorn proj.wsgi:application (or whatever)
fi
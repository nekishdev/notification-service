#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

if [[ $(python manage.py showmigrations movies | grep '\[ \] 0001_initial') ]]; then
    python manage.py migrate --fake movies 0001
fi

python manage.py migrate \
  && python manage.py collectstatic --no-input \
  && uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini

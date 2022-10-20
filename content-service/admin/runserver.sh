#!/bin/bash

set -e

if [[ $(python manage.py showmigrations movies | grep '\[ \] 0001_initial') ]]; then
    python manage.py migrate --fake movies 0001
fi

python manage.py migrate \
  && python manage.py collectstatic --no-input \
  && python manage.py runserver ${RUNSERVER_ADDRESS}
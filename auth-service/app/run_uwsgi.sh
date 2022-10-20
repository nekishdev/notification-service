#!/usr/bin/env bash

uwsgi --master \
  --single-interpreter \
  --workers $WORKERS \
  --gevent $ASYNC_CORES \
  --protocol $PROTOCOL \
  --socket $APP_HOST:$APP_PORT \
  --module wsgi_app:app

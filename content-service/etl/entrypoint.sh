#!/usr/bin/env bash

set -e

printf "Waiting Postgres...\n"
while ! nc -z $PG_WAIT_HOST $PG_WAIT_PORT; do
      sleep 0.1
done
printf "Postgres: OK\n"

printf "Waiting Elasticsearch...\n"
while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      sleep 0.1
done
printf "Elasticsearch: OK\n"

cd /opt/app \
  && python start_loaders.py
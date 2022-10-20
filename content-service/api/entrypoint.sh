#!/usr/bin/env bash

set -e

printf "Waiting Redis...\n"
while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
done
printf "Redis: OK\n"

printf "Waiting Elasticsearch...\n"
while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      sleep 0.1
done
printf "Elasticsearch: OK\n"

exec "$@"
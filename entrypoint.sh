#!/bin/bash

sleep 5

python manage.py migrate

python manage.py collectstatic --noinput

python add_sample_data.py

exec "$@"
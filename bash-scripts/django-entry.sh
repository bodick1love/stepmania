#!/bin/sh

echo start migrations
python stepmania/manage.py makemigrations --noinput
python stepmania/manage.py migrate --noinput

# Execute the container's main CMD
exec "$@"

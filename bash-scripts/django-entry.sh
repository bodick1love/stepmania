#!/bin/sh

echo start migrations
python stepmania/manage.py makemigrations --noinput
python stepmania/manage.py migrate --noinput
python stepmania/manage.py collectstatic --noinput


# Execute the container's main CMD
exec "$@"

#!/bin/sh

echo start migrations
python stepmania/manage.py makemigrations --noinput
python stepmania/manage.py migrate --noinput

python stepmania/manage.py loaddata stepmania/data.json

# Execute the container's main CMD
exec "$@"

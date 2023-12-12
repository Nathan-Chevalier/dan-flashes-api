#!/bin/bash
rm db.sqlite3
rm -rf ./danflashesapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations danflashesapi
python3 manage.py migrate danflashesapi
python3 manage.py loaddata user
python3 manage.py loaddata token
python3 manage.py loaddata pattern
python3 manage.py loaddata color
python3 manage.py loaddata flashes_user
python3 manage.py loaddata shirt
python3 manage.py loaddata shirt_pattern
python3 manage.py loaddata shirt_favorite

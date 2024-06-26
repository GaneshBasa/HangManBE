#!/usr/bin/bash

echo "Building Project Packages..."
python3 -m pip install -r requirements.txt

echo "Migrating Database..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting Static Files..."
python3 manage.py collectstatic --noinput

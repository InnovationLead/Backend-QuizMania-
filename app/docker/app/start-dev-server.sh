#!/bin/bash
echo $(pwd)
echo $(ls -l)
echo $(ls -l ./app)
echo "Running migrations..."
python3 manage.py migrate
echo "Starting server..."
python3 manage.py runserver 0.0.0.0:8000
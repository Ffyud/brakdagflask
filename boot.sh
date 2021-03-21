#!/bin/bash
source venv/bin/activate
ls
cd app
flask --version
# flask db upgrade
# flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - brakdagflask:app
exec python3 nieuws-ophalen.py http://95.217.165.225:8000
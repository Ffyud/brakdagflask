#!/bin/sh
source venv/bin/activate
flask --version
# flask db upgrade
# flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - brakdagflask:app
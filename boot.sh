#!/bin/bash
source venv/bin/activate
ls
cd app
flask --version
# flask db upgrade
# flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - brakdagflask:app

#!/bin/bash
source venv/bin/activate
exec python3 nieuws-ophalen.py http://brakdagflask:5000 & nieuws-match.py http://brakdagflask:5000
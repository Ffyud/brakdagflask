FROM python:3.8

RUN adduser --disabled-login brakdagflask

WORKDIR /home/brakdagflask

COPY requirements.txt requirements.txt
RUN python -m venv venv
# RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP=brakdagflask

RUN chown -R brakdagflask:brakdagflask ./
USER brakdagflask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
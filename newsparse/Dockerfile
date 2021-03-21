FROM python:3.8

RUN adduser --disabled-login newsparse

WORKDIR /home/newsparse

RUN python -m venv venv

COPY nieuws-ophalen.py nieuws-ophalen.py
COPY boot.sh boot.sh
RUN chmod +x boot.sh

RUN chown -R newsparse:newsparse ./
USER newsparse

ENTRYPOINT ["./boot.sh"]
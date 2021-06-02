FROM python:3.8

RUN adduser --disabled-login newsparse

WORKDIR /home/newsparse

COPY ./newsparse/requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY ./newsparse/nieuws-ophalen.py nieuws-ophalen.py
COPY ./newsparse/boot.sh boot.sh
RUN chmod +x boot.sh

RUN chown -R newsparse:newsparse ./
USER newsparse

EXPOSE 3300
ENTRYPOINT ["./boot.sh"]
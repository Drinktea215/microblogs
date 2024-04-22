FROM python:3.12

COPY migrations migrations

COPY src src

COPY .env .env

COPY alembic.ini alembic.ini

COPY requirements-ci.txt requirements.txt

COPY run.sh run.sh

COPY supervisord.ini supervisord.ini

COPY uwsgi.ini uwsgi.ini

WORKDIR .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

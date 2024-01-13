FROM python:3.11
COPY . .
#COPY migrations migrations
#COPY src src
#COPY static static
#COPY tests tests
#COPY alembic.ini alembic.ini
#COPY pyproject.toml pyproject.toml
#COPY requirements.txt requirements.txt
#COPY run.sh run.sh
#COPY supervisord.ini supervisord.ini
#COPY uwsgi.ini uwsgi.ini
#COPY .env .env
WORKDIR .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

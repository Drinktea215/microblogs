FROM python:3.11

COPY src src

COPY migrations migrations

COPY alembic.ini alembic.ini

COPY supervisord.ini supervisord.ini

COPY uwsgi.ini uwsgi.ini

COPY __init__.py __init__.py

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

WORKDIR /src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

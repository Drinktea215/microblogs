FROM python:3.11

COPY . .

WORKDIR .

RUN python3 -m pip install -r requirements.txt

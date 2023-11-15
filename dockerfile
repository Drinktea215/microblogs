FROM python:3.11

COPY . .

WORKDIR .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

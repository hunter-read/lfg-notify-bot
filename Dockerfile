FROM python:3.11-alpine
LABEL maintainer="hunter@readpnw.dev"

WORKDIR /code

COPY requirements.txt .
COPY src/ .

RUN pip install --user -r requirements.txt
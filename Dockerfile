FROM python:3.11

WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r ../requirements.txt

COPY /backend /app/backend/

FROM python:3.12

WORKDIR /app

ENV PYTHONPATHBUFFERED = 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

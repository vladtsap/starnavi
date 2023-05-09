FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DEBUG=TRUE

WORKDIR /app

COPY . /app

RUN chmod a+x docker-entrypoint.sh && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

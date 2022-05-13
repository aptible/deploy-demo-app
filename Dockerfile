FROM ghcr.io/multi-py/python-gunicorn:py3.10-slim-latest

# first row needed for postgres/sqlalchemy
# second row needed for common libraries used (ex: gcc)
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev libssl-dev libpq-dev postgresql-client \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY .aptible /

WORKDIR /app
ADD pyproject.toml /app/
ADD setup.cfg /app/
ADD ./.aptible /.aptible

RUN pip install -e .[dev]
ADD app/ /app/

ENV PORT 5000
EXPOSE 5000

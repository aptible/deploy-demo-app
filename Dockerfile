FROM python:3-slim

# first row needed for postgres/sqlalchemy
# second row needed for common libraries used (ex: gcc)
RUN apt-get update && apt-get install -y \
    build-essential  \
    libcurl4-openssl-dev  \
    libpq-dev \
    libssl-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ADD ./.aptible /.aptible

WORKDIR /app
ADD pyproject.toml /app/
ADD setup.cfg /app/

RUN pip install -e .[install_requires]
ADD app/ /app/

ENV PORT 5000
EXPOSE 5000

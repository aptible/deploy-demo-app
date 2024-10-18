FROM python:3.12-slim

# build-essential is needed for various python dependencies (gcc + others are in build-essential)
# libpq-dev is needed for psycopg2 to be installed
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# The .aptible directory contains an .aptible.yml file and a Procfile
# 1. The .aptible.yml file has a `before_release` which runs data migrations in an isolated container before a launch
#    Details about .aptible.yml files can be found here - https://deploy-docs.aptible.com/docs/aptible-yml
# 2. The Procfile has two processes (a background worker and a web server).
#    Details about Procfiles can be found here: https://deploy-docs.aptible.com/docs/defining-services#explicit-services-procfiles
ADD ./.aptible /.aptible

WORKDIR /app
ADD requirements.txt /app/

RUN pip install -r requirements.txt
ADD app/ /app/

ENV PORT 5000
EXPOSE 5000

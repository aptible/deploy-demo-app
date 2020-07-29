# Dockerfile
FROM python:3.5-slim

# Add requirements.txt ONLY, then run pip install, so that Docker cache won't
# be invalidated when changes are made to other repo files

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# WARNING: the following is applicable only for Direct Docker Image Deployment
# For Dockerfile (git-based) deployments, only the Procfile and .aptible.yml in the root of the repository matter
# See https://www.aptible.com/documentation/deploy/reference/apps/services/procfiles.html#procfiles
# and https://www.aptible.com/documentation/deploy/reference/apps/aptible-yml.html#aptible-yml

ADD Procfile /.aptible/
ADD migrations /.aptible/aptible.yml

# Add repo contents to image
ADD app/ /app/

ENV PORT 5000
EXPOSE 5000

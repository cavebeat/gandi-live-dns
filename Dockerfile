
FROM python:3.8-slim as builder
RUN apt-get update \
&& apt-get install gcc build-essential cron -y \
&& apt-get clean

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY . .

# entrypoint and cron after https://blog.knoldus.com/running-a-cron-job-in-docker-container/
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh

#todo make smaller by using the building image as the start and then copying over the compiled binaries for brotlipy
## https://www.rockyourcode.com/create-a-multi-stage-docker-build-for-python-flask-and-postgres/
### base image
#FROM python:3.7.5-slim-buster AS compile-image
#
### install dependencies
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends gcc
#
### virtualenv
#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#
### add and install requirements
#RUN pip install --upgrade pip && pip install pip-tools
#COPY ./requirements.in .
#RUN pip-compile requirements.in > requirements.txt && pip-sync
#RUN pip install -r requirements.txt
#
### build-image
#FROM python:3.7.5-slim-buster AS runtime-image
#
### copy Python dependencies from build image
#COPY --from=compile-image /opt/venv /opt/venv
#
### set working directory
#WORKDIR /usr/src/app
#
### add app
#COPY . /usr/src/app
#
#ENV PATH="/opt/venv/bin:$PATH"
#
#
#
#COPY . .
#CMD [ "python", "./gandi-live-dns.py" ]
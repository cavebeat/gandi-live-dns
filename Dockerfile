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


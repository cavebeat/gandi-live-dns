#!/bin/bash

# todo this really should run in a way that logs the output of the jobs to the console
# todo option A https://stackoverflow.com/questions/45395390/see-cron-output-via-docker-logs-without-using-an-extra-file
# todo if we do, also add a production flag (or a debugging one) that only outputs a single print line when a DNS IP is updated

# Start the run once job.
echo "gandi-dns-live container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env
* * * * * cd /usr/src/app && python /usr/src/app/gandi-live-dns.py >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
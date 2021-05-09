#!/bin/bash

# Start the run once job.
echo "gandi-dns-live container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule for every minute, and follow the cron log
echo "SHELL=/bin/bash
BASH_ENV=/container.env
* * * * * cd /usr/src/app && python /usr/src/app/gandi-live-dns.py 2>/proc/1/fd/2 >&2
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
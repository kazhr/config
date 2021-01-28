FROM frolvlad/alpine-python3

COPY crontab /var/spool/cron/crontabs/root
COPY show_date.py /

CMD ["crond", "-f", "-d", "8"]
# BusyBox v1.31.1 () multi-call binary.
#
# Usage: crond -fbS -l N -d N -L LOGFILE -c DIR
#
# 	-f	Foreground
# 	-b	Background (default)
# 	-S	Log to syslog (default)
# 	-l N	Set log level. Most verbose 0, default 8
# 	-d N	Set log level, log to stderr
# 	-L FILE	Log to FILE
# 	-c DIR	Cron dir. Default:/var/spool/cron/crontabs

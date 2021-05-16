#!/bin/bash

HOST="localhost"
USER="telnet"
PASS="password"
LOG_FILE=$(mktemp)

# main
( sleep 1; echo "$USER"; \
  sleep 1; echo "$PASS"; \
  sleep 1; echo "id";    \
  sleep 1; echo "quit";  \
)| telnet $HOST &>$LOG_FILE

# remove carriage Return
sed -i -e 's/\r//g' $LOG_FILE

# remove "ESC Code Sequence: request cursor position"
sed -i -e 's/\x1b\[6n//' $LOG_FILE

# show
cat $LOG_FILE

# finalize
rm -f $LOG_FILE

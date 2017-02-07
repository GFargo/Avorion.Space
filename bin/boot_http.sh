#! /usr/bin/bash

# We want to boot our pythong server in a detached screen
# to keep it out of the way and running at all times
if [ -z "$STY" ]; then exec screen -dm -S simpleHttp /bin/bash "$0"; fi

cd /var/www/
python -m SimpleHTTPServer 80


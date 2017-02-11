#! /usr/bin/bash
#
#      ___   ____    ____  ______   .______       __    ______   .__   __.
#     /   \  \   \  /   / /  __  \  |   _  \     |  |  /  __  \  |  \ |  |
#    /  ^  \  \   \/   / |  |  |  | |  |_)  |    |  | |  |  |  | |   \|  |
#   /  /_\  \  \      /  |  |  |  | |      /     |  | |  |  |  | |  . `  |
#  /  _____  \  \    /   |  `--'  | |  |\  \----.|  | |  `--'  | |  |\   |
# /__/     \__\  \__/     \______/  | _| `._____||__|  \______/  |__| \__|
#
############################################################################
# Simple HTTP Server via Python
############################################################################

# Boot the server in a detached screen to keep it active after exit
# conditional checks the server screen isn't already running
if [ -z "$STY" ]; then exec screen -dm -S simpleHttp /bin/bash "$0"; fi

echo "\n....booting SimpleHTTPServer on port 80..."

# Bootup the HTTP server
cd /var/www/
python -m SimpleHTTPServer 80

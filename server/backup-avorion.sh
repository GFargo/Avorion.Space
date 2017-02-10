#!/bin/bash
#
#      ___   ____    ____  ______   .______       __    ______   .__   __.
#     /   \  \   \  /   / /  __  \  |   _  \     |  |  /  __  \  |  \ |  |
#    /  ^  \  \   \/   / |  |  |  | |  |_)  |    |  | |  |  |  | |   \|  |
#   /  /_\  \  \      /  |  |  |  | |      /     |  | |  |  |  | |  . `  |
#  /  _____  \  \    /   |  `--'  | |  |\  \----.|  | |  `--'  | |  |\   |
# /__/     \__\  \__/     \______/  | _| `._____||__|  \______/  |__| \__|
#

# Setup our variables
TMP_DIR="/tmp/"
DATE=$(date +"%d-%m-%Y_%H%M")
BKP_FILE="$TMP_DIR/AvorionBackup_$DATE.tar"
BKP_DIRS="/home/steam/.avorion"
DROPBOX_UPLOADER=/home/steam/dropbox_uploader.sh

tar cf "$BKP_FILE" $BKP_DIRS
gzip "$BKP_FILE"

# Send backup to dropbox
$DROPBOX_UPLOADER -f /home/steam/.dropbox_uploader upload "$BKP_FILE.gz" /

# Remove gzip after we've uploaded to dropbox
rm -fr "$BKP_FILE.gz"
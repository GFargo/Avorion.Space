#!/bin/bash
#
#      ___   ____    ____  ______   .______       __    ______   .__   __.
#     /   \  \   \  /   / /  __  \  |   _  \     |  |  /  __  \  |  \ |  |
#    /  ^  \  \   \/   / |  |  |  | |  |_)  |    |  | |  |  |  | |   \|  |
#   /  /_\  \  \      /  |  |  |  | |      /     |  | |  |  |  | |  . `  |
#  /  _____  \  \    /   |  `--'  | |  |\  \----.|  | |  `--'  | |  |\   |
# /__/     \__\  \__/     \______/  | _| `._____||__|  \______/  |__| \__|
#
############################################################################
# Shell Script to backup Avorion galaxy files
#
# Additional Parameters:
# $1 - Custom Name for Backup
# $2 - Additional directories to backup
#
############################################################################

# Setup location to store temp backups on server
# before sending up to dropbox
TMP_DIR="/tmp/"

# Unique date string for filename
DATE=$(date +"%d-%m-%Y_%H%M")

# Use custom for backup if passed into script
if [ -z "$1" ]; then
	BKP_FILE="$TMP_DIR/AvorionBackup_$DATE.tar"
else
	BKP_FILE="$TMP_DIR/AvorionBackup__$1_$DATE.tar"
fi

BKP_DIRS="/home/steam/.avorion $2"
DROPBOX_UPLOADER=/home/steam/dropbox_uploader.sh

tar cf "$BKP_FILE" $BKP_DIRS
gzip "$BKP_FILE"

# Send backup to dropbox
$DROPBOX_UPLOADER -f /home/steam/.dropbox_uploader upload "$BKP_FILE.gz" /

# Remove gzip after we've uploaded to dropbox
rm -fr "$BKP_FILE.gz"


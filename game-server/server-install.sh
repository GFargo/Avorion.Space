#!/bin/bash
#
#      ___   ____    ____  ______   .______       __    ______   .__   __.
#     /   \  \   \  /   / /  __  \  |   _  \     |  |  /  __  \  |  \ |  |
#    /  ^  \  \   \/   / |  |  |  | |  |_)  |    |  | |  |  |  | |   \|  |
#   /  /_\  \  \      /  |  |  |  | |      /     |  | |  |  |  | |  . `  |
#  /  _____  \  \    /   |  `--'  | |  |\  \----.|  | |  `--'  | |  |\   |
# /__/     \__\  \__/     \______/  | _| `._____||__|  \______/  |__| \__|
#                                                                                                                                                             #
#
############################################################################
# Shell Script to setup Avorion dedicated server on Linux
############################################################################




# Download Dropbox Uploader
# @see https://github.com/andreafabrizi/Dropbox-Uploader

curl "https://raw.githubusercontent.com/andreafabrizi/Dropbox-Uploader/master/dropbox_uploader.sh" -o dropbox_uploader.sh
chmod +x dropbox_uploader.sh

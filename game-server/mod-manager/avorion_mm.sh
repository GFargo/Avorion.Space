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
# Avorion Mod Manager
############################################################################


cat example.list | xargs sudo apt-get -y install

apt-get install <package name> -y


# ------------------------------------------------------------
# Setup Environment
# ------------------------------------------------------------
PATH=/usr/bin:/bin
umask 022
PDIR=${0%`basename $0`}
ZIP_FILENAME=Unpacked.zip

# Number of lines in this script file (plus 1)
SCRIPT_LINES=64

# Run /bin/sum on your binary and put the two values here
SUM1=07673
SUM2=2




## Using Git for Mod Reversion Control
#
# create
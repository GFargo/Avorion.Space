#!/bin/bash
#
#      ___   ____    ____  ______   .______       __    ______   .__   __.
#     /   \  \   \  /   / /  __  \  |   _  \     |  |  /  __  \  |  \ |  |
#    /  ^  \  \   \/   / |  |  |  | |  |_)  |    |  | |  |  |  | |   \|  |
#   /  /_\  \  \      /  |  |  |  | |      /     |  | |  |  |  | |  . `  |
#  /  _____  \  \    /   |  `--'  | |  |\  \----.|  | |  `--'  | |  |\   |
# /__/     \__\  \__/     \______/  | _| `._____||__|  \______/  |__| \__|
#

cp linux64/steamclient.so ./steamclient.so

# Update these variables with custom settings
SERVER_NAME="Avorion.Space"
GALAXY_NAME="avorion_galaxy"
MAX_LOGS="10"
USE_STEAM_NETWORK="1"
IS_PUBLIC="1"

ADMIN_IDS="14443998"

MAX_PLAYERS="20"
COLLISION_DMG="0.8"
DIFFICULTY="0"
# INFINITE_RESOURCES=""


# Check what variables to pass to server
# @see http://wiki.avorion.net/index.php?title=Server#Command_Line_Options
function server_args {

	# list of arguments passed to server
	args=""

	# Check for custom galaxy name
	if [ -z "$SERVER_NAME" ]; then
		args="$args --server-name $SERVER_NAME"
	fi
	# Check for custom galaxy name
	if [ -z "$GALAXY_NAME" ]; then
		args="$args --galaxy-name $GALAXY_NAME"
	else
		args="$args --galaxy-name avorion_galaxy"
	fi
	# Check if public server
	if [ -z "$IS_PUBLIC" ]; then
		args="$args --public $IS_PUBLIC"
	fi
	# Do we want to use steam network?
	if [ -z "$USE_STEAM_NETWORK" ]; then
		args="$args --use-steam-networking $USE_STEAM_NETWORK"
	fi
	# Check for Admin IDs
	if [ -z "$ADMIN_IDS" ]; then
		args="$args --admin $ADMIN_IDS"
	fi
	# Check max players permitted on server
	if [ -z "$MAX_PLAYERS" ]; then
		args="$args --max-players $MAX_PLAYERS"
	fi
	# Check max number of logs to store
	if [ -z "$MAX_LOGS" ]; then
		args="$args --max-logs $MAX_LOGS"
	fi
	# Check collision damage ratio, range between 0 and  1
	if [ -z "$COLLISION_DMG" ]; then
		args="$args --collision-damage $COLLISION_DMG"
	fi
	# Check if difficulty has been set
	if [ -z "$DIFFICULTY" ]; then
		args="$args --difficulty $DIFFICULTY"
	fi
	# Check for Build Mode
	if [ -z "$INFINITE_RESOURCES" ]; then
		args="$args --infinite-resources $INFINITE_RESOURCES"
	fi

	# echo out server args
	echo "$args"
}


# Start up Server
bin/AvorionServer $( server_args )

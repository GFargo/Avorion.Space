"""Mod Manager for Avorion.

This tool allows to search for mods in a central repository and installation of these mods to a local Avorion client or server.
"""

from __future__ import print_function
import argparse
import avorion_mm

def start():
    """Start the CLI interface for the mod manager."""
    ## Define CLI arguments
    parser = argparse.ArgumentParser(description='Allow for polling of central mod repository and installation, update and uninstallation of mods. Also checks mod versions and checks compatibility with other mods and game. Additionally allows backup of local game version.')
    parser.add_argument('-v', '--verbose',        action='store_true', dest='verbose',    help='Start with verbose mode enabled')
    parser.add_argument('-r', '--set-repository', action='store',      dest='repository', help='Set repository URL to fetch mods from. (e.g. "https://github.com/Strongground/avorion_mods")')
    parser.add_argument('-d', '--set-database',   action='store',      dest='database',   help='Set name of local database, if existing it will be overwritten (e.g. "database")')
    args = parser.parse_args()

    if not args.repository:
        repository = 'https://raw.githubusercontent.com/Strongground/avorion_mods/master/'
    else:
        repository = args.repository
    if not args.database:
        database_name = 'appdata'
    else:
        database_name = args.database

    modmanager = avorion_mm.AvorionModManager(verbose=args.verbose, database_name=database_name, repository=repository)


start()

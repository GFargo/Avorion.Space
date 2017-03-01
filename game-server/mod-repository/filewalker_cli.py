"""Mod repository list creation tool.

This tool is designed to be started in regular intervals and pull all changes from a repository containing Avorion mod files.
If there where changes, it compiles a json formatted list containing all modinfo-content and merges, commits and pushes it.
"""

from __future__ import print_function
import argparse
import filewalker

def start():
    """Start the CLI interface for the mod list tool."""
    ## Define CLI arguments
    parser = argparse.ArgumentParser(description='Pull changes from Avorion mod repository. If changes where pulled, compile a json formatted list of the modfiles used to descibe each mod and push it back to the repository.')
    parser.add_argument('-v', '--verbose',        action='store_true', dest='verbose',    help='Start with verbose mode enabled')
    parser.add_argument('-r', '--set-repository', action='store',      dest='repository', help='Set repository URL to fetch mods from. Default is "https://github.com/Strongground/avorion_mods.git"')
    parser.add_argument('-p', '--set-localpath',  action='store',      dest='local',      help='Set local path to repositories .git-file. As to yet the local repository needs to be existing - this script does not cover cloning yet.')
    args = parser.parse_args()

    if not args.repository:
        repository = 'https://github.com/Strongground/avorion_mods.git'
    else:
        repository = args.repository

    walker = filewalker.FileWalker(verbose=args.verbose, local_repo_path=args.local, remote_repository=repository)

start()

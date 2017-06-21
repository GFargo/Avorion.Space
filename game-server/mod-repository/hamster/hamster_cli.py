"""HAMSTER (helpful avorion mod submission tool for server) - Serve a simple webform to create the modinfo JSON file for a Avorion modification automatically based on its input.

Optionally trigger the filewalker tool to create a updated modlist from all modinfo files in a centralized repository.
"""

from __future__ import print_function
# from pprint import pprint
import argparse
from hamster import Hamster

def start():
    """The main function to start the HAMSTER server."""
    ## Define CLI arguments
    parser = argparse.ArgumentParser(description='Serve a simple webform to create the modinfo JSON file for a Avorion modification automatically based on its input. By default exposes itself on port 8585 and enabled debug printouts. Use --live to make it available on port 80 - you need root access for this!')
    parser.add_argument('-v', '--verbose',  action='store_true', dest='verbose',  help='start with verbose mode enabled')
    parser.add_argument('-D', '--Debug',    action='store_true', dest='debug',    help='start HAMSTER in debug mode. This does expose the server on port 8585 and enables debug printouts in the code as well as mockup environments for certain classes and modules.')
    parser.add_argument('-i', '--host',     action='store',      dest='host',     help='server will be available on this hostname (e.g. 192.168.2.105:8585)')
    args = parser.parse_args()

    if args.host:
        host = args.host.split(':')[0]
        port = args.host.split(':')[1]
    else:
        # host = '192.168.2.105' You stupid or what?
        host = 'localhost'
        port = '8585'

    hamster = Hamster(verbose=args.verbose, debug_mode=args.debug)
    hamster.start(args.debug, host, port)

start()

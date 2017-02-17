"""Handle all function calls to the mod manager, interface-agnostic."""

from __future__ import print_function
from pprint import pprint
from urllib import urlopen
import shelve
import simplejson

class AvorionModManager(object):
    """Main class to handle all function calls to mod manager from any interface."""

    def __init__(self, verbose, database_name, repository):
        """Comment only serves to make PEP happy..."""
        self.database_name = database_name
        self.verbose = verbose
        self.main_repository_url = repository
        self.main_mod_list = 'modlist.json'
        try:
            self.database = shelve.open(self.database_name, writeback=True)
        except Exception as e:
            print('Error opening shelf: '+str(e))
            raise
        self.get_mod_list()

    def close_db(self):
        """Close the currently open shelve database."""
        try:
            self.database.close()
            return True
        except Exception as e:
            print('Error closing shelf: '+str(e))
            raise

    def get_mod_list(self, save_to_shelve=True):
        """Get a JSON list of available mods from the central mods repository."""
        mod_list_url = self.main_repository_url+self.main_mod_list
        response = urlopen(mod_list_url)
        mods = simplejson.load(response)
        if self.verbose:
            for mod in mods:
                print('Found mod: '+mods[mod]['name']+' by '+mods[mod]['author'])
        if save_to_shelve:
            print('Attempt to save into local DB "'+self.database_name+'"')
            self.database['mods'] = mods
        else:
            return dict(mods)

    def list_mods(self):
        """Return all mods from shelf as dict."""
        try:
            return dict(self.database[0])
        except Exception as e:
            print('Error getting mods: '+str(e))
            raise

    def list_mod(self, mod_id):
        """Get a specific mod from shelf and return as dict."""
        try:
            for mod in self.database[0]:
                if mod['id'] == mod_id:
                    return dict(mod)
        except Exception as e:
            print('Error getting mod with id '+str(mod_id)+': '+str(e))
            raise

## TESTING
#
# local_mod_manager = AvorionModManager()
#
# local_mod_manager.get_mod_list(save_to_shelve=False)
#
# local_mod_manager.close_db()

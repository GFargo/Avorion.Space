"""Generate a json file based off a file structure containing json files describing mods."""

from __future__ import print_function
# from pprint import pprint
# import io
import os
import subprocess
# import sys
# import zipfile
# import datetime
import pygit2
import simplejson

class MyCallbacks(pygit2.RemoteCallbacks):
    """Inherited class for remote callbacks."""

    # This is not needed at the moment - see comment for push()-method
    # def credentials(self, url, username_from_url, allowed_types):
    #     """Credential callback for remote authentication.
    #
    #     These are called from pygit2 on various situations and are overriden here.
    #     """
    #     userpass = pygit2.UserPass('Strongground', '1234')
    #     return userpass
    #
    # def push_update_reference(self, refname, message):
    #     """Callback for push progress and success notification from remote."""
    #     if refname and message:
    #         print("Got the following from remote: "+refname+": "+message)

class FileWalker(object):
    """Traverse a folder tree and generate a JSON based on folder names and JSON files in the folders."""

    def __init__(self, verbose, remote_repository, local_repo_path, output_file_name='modlist.json'):
        """Comment only serves to make PEP happy..."""
        self.callbacks = MyCallbacks()
        self.verbose = verbose
        self.output_file_name = output_file_name
        local_repo = pygit2.Repository(local_repo_path)
        if len(local_repo.remotes) <= 0:
            local_repo.remotes.create('origin', remote_repository)

        # If pull returns True, changes have been pulled.
        if self.pull(local_repo):
            # There where changes in origin, that have been pulled.
            # Now create a new modlist out of the changed file structure in the repo folder.
            self.create_commit(local_repo)
            if self.verbose:
                print('Attempted to create commit with merged changes from remote repository')
            self.push(local_repo)
        else:
            # Nothing to do here.
            if self.verbose:
                print('Up to date, do nothing')

    def create_commit(self, repo):
        """Commit the newly generated modlist.json."""
        if repo.head_is_unborn:
            parent = []
        else:
            parent = [repo.head.target]
        self.generate_json(repo.workdir)
        repo.index.add_all()
        user = repo.default_signature
        tree = repo.index.write_tree()
        commit = repo.create_commit('refs/heads/master', user, user, 'Automatically updated modlist.json', tree, parent)
        # Apparently the index needs to be written after a write tree to clean it up.
        # https://github.com/libgit2/pygit2/issues/370
        repo.index.write()
        parent = [commit]

    def pull(self, repo, remote_name='origin', branch='master'):
        """Pull changes from origin."""
        for remote in repo.remotes:
            if remote.name == remote_name:
                remote.fetch()
                remote_master_id = repo.lookup_reference('refs/remotes/origin/%s' % (branch)).target
                merge_result, _ = repo.merge_analysis(remote_master_id)
                # Up to date, do nothing
                if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                    return False
                # We can just fastforward
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                    repo.checkout_tree(repo.get(remote_master_id))
                    try:
                        master_ref = repo.lookup_reference('refs/heads/%s' % (branch))
                        master_ref.set_target(remote_master_id)
                    except KeyError:
                        repo.create_branch(branch, repo.get(remote_master_id))
                    repo.head.set_target(remote_master_id)
                    return True
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                    repo.merge(remote_master_id)
                    if repo.index.conflicts is not None:
                        for conflict in repo.index.conflicts:
                            print('Conflicts found in: '+str(conflict[0].path))
                        raise AssertionError('Conflicts, ahhhhh!!')
                    user = repo.default_signature
                    tree = repo.index.write_tree()
                    commit = repo.create_commit('refs/heads/master', user, user, 'Merge!', tree, [repo.head.target, remote_master_id])
                    # We need to do this or git CLI will think we are still merging.
                    repo.state_cleanup()
                    return True
                else:
                    raise AssertionError('Unknown merge analysis result')

    def push(self, repo):
        """Push the new modlist.json to origin."""
        # This shit is not working - but isn't throwing any errors either
        # original call was:
        # def push(self, repo, remote_name='origin', ref=['refs/heads/master:refs/heads/master']):
        # for remote in repo.remotes:
        #     if remote.name == remote_name:
        #         remote.push(ref, callbacks=self.callbacks)
        # first make sure we have 'master' branch active
        repo.checkout('refs/heads/master')
        # move to repository folder for git command to work properly
        try:
            subprocess.Popen(['git', 'push'], cwd=repo.workdir, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

    def generate_json(self, path):
        """Generate JSON file from the file structure and contents in given local_repo/mods folder."""
        modlist = []
        modspath = str(path+'mods/')
        for curDir, _, subFiles in os.walk(modspath):
            if self.verbose:
                print('Processing '+os.path.basename(curDir))
            for modfile in subFiles:
                if modfile == 'modinfo.json':
                    modinfo = open(curDir+"/"+modfile)
                    modfile_content = simplejson.load(modinfo)
                    if isinstance(modfile_content, dict):
                        # Contains only one mod, write straight away into modlist
                        modlist.append(modfile_content)
                    elif isinstance(modfile_content, list):
                        # Contains a list of mods, iterate and write each to modlist, adding a package attribute to each
                        for mod in modfile_content:
                            mod['package'] = os.path.basename(curDir)
                            modlist.append(mod)
                    modinfo.close()
        newfile = open(str(path)+'modlist.json', mode='w+')
        simplejson.dump(modlist, newfile)

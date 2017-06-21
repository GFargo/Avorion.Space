# -*- coding: utf-8 -*-
#!/usr/bin/python
"""Offe a webform and generate a JSON from submissions to this form."""
from __future__ import print_function
from pprint import pprint
import string
from urlparse import urlparse
import os
import yaml
import simplejson
from bottle import Bottle, template, request, static_file, redirect, debug

# @TODO Render simple webform with all user submitted fields from the modinfo.json
# @TODO Route the output of any submission from the page trough a sanitizer module and validate it to make sure nothing bad can get into the modinfo.json
    # * Only allow for certain tlds in the links to the modfiles (like github)
    # * Filter any special characters. Allowed chars: A-Z,a-z,Whitespace,-,
# @TODO Check if "package" option was checked and if a folder with the given package name exists
    # * If not, return validation error to the user and do not proceed
    # * If yes,
        # 1. open the folder/modinfo.json
        # 2. decode file content into object
        # 3. append the info from the form to the object (including the package-value)
        # 4. encode object into file modinfo.json again and save
# @TODO If "package" option was not checked:
    # * Create folder from name of the submitted mod
    # * Inside, create modinfo.json file handle
# @TODO Trigger creation of modinfo.json generation based on the formdata:
    # * Create object directly off the values
    # * Encode this object into JSON
# @TODO Eventually trigger the modlist.json generation from filewalker.py

class Hamster(object):
    """The "Helpful Avorion Mod Submission Tool for sERvers".

    The premise of this script is that modinfo files are read and processed by a client side mod manager.
    This tool however allows mod ceators to upload their mod information to a central repository so that the
    mod manager knows about it in the first place.

    It serves a simple web page containing a form that allows a mod creator to supply all necessary information to let the script generate a modinfo.json, containing all
    information to handle the mod via mod manager. The modinfo files are stored in a central git repository, this and the generation of a modlist.json containing the combined information
    of all modinfo.json files is handled by filewalker.py script. This tool, as its name already indicates, should be run on a server. It brings its own tiny webserver.
    """

    def __init__(self, verbose, debug_mode):
        """Inititalize hamster."""
        self._app = Bottle()
        self.verbose = verbose
        self._route()
        self.strings = self.load_string_file('strings.yml')
        self.allowed_chars = string.ascii_letters + string.digits + '_' + '-' + ' '
        self.allowed_version_chars = string.ascii_letters + string.digits + '_' + '-' + ' ' + '.'
        self.allowed_urls = 'github', 'bitbucket', 'gitlab', 'avorion.net'
        self.allowed_file_ext = '.lua'

    ### route method
    def _route(self):
        # framework
        self._app.route('/js/<filename>', method="GET", callback=self.js_static)
        self._app.route('/js/bootstrap/<filename>', method="GET", callback=self.js_static_bootstrap)
        self._app.route('/img/<filename>', method="GET", callback=self.img_static)
        self._app.route('/css/<filename>', method="GET", callback=self.css_static)
        self._app.route('/fonts/bootstrap/<filename>', method="GET", callback=self.fonts_static_bootstrap)
        self._app.route('/fonts/<filename>', method="GET", callback=self.fonts_static)
        # errors
        self._app.error(code=500)(self.error500)
        self._app.error(code=404)(self.error404)
        # form page
        self._app.route('/', method="GET", callback=self.show_form)
        self._app.route('/', method="POST", callback=self.process_form)

    #### Helper methods
    def start(self, debug_mode, host, port):
        """Default start for server."""
        if debug_mode:
            debug(True)
            if self.verbose:
                print('Debug mode')
        self._app.run(host=host, port=port)

    def load_string_file(self, filename):
        """Load localizable strings."""
        file_handle = open(filename)
        string_file = yaml.safe_load(file_handle)
        file_handle.close()
        return string_file

    def validate_form(self, form_input):
        """Check if given form data is correct, valid and free of malicious stuff. Return all findings as object."""
        result = dict()
        result['check'] = True
        result['error_field'] = []
        result['error_reason'] = []
        # Check that only allowed characters are contained
        for input_element in form_input:
            input_element_value = str(form_input.get(input_element))
            validation_type = self.get_validation_type(input_element)
            print('============================================================')
            print('Testing form element "'+input_element+'" containing value: "'+input_element_value+'", of type "'+validation_type+'". This field is mandatory: '+str(self.get_mandatory(input_element)))
            # mandatory fields cannot be empty, so treat this like a proper input_type and check it first
            if self.get_mandatory(input_element):
                if self.length_zero(input_element_value):
                    # element mandatory but empty
                    result = self.validation_error(result, input_element, 'no-zero-length')
                    continue
            # validation for input text type
            if validation_type in ['text', 'version']:
                print('Validation type "'+validation_type+'" found')
                # check against valid characters
                print('Testing value "'+input_element_value+'" against allowed characters...')
                if validation_type == 'text':
                    if self.invalid_chars(input_element_value, self.allowed_chars):
                        # invalid chars found
                        print('Text-Validation: Invalid Character found')
                        result = self.validation_error(result, input_element, 'invalid-char')
                    else:
                        print('Text-Validation: Everything okay')
                else:
                    # assuming validation_type of 'version' then
                    if self.invalid_chars(input_element_value, self.allowed_version_chars):
                        # invalid chars found
                        print('Version-Validation: Invalid Character found')
                        result = self.validation_error(result, input_element, 'invalid-version')
                    else:
                        print('Version-Validation: Everything okay')
            elif validation_type == 'url':
                print('Validation type "'+validation_type+'" found')
                # check against whitelist of domains allowed
                print('Testing value "'+input_element_value+'" against allowed domains...')
                if not self.may_be_url(input_element_value, self.allowed_urls):
                    print('URL-Validation: URL contains no domain found in whitelist.')
                    result = self.validation_error(result, input_element, 'invalid-url')
                else:
                    print('URL-Validation: Everything okay')
            elif validation_type == 'file':
                print('Validation type "'+validation_type+'" found')
                # check against whitelist of domains allowed
                print('Checking value "'+input_element_value+'" for allowed extension...')
                if not self.may_be_url(input_element_value, self.allowed_file_ext, True):
                    print('File-URL-Validation: URL contains extension of supposed mod file.')
                    result = self.validation_error(result, input_element, 'no-file-given')
                else:
                    print('File-URL-Validation: Everything okay')

        # Return the result object
        print('============================================================')
        print('Result object of validation:')
        pprint(result)
        return result

    #### Validators

    def length_zero(self, input_string):
        """Return True if length of given string is greater than 0, False otherwise."""
        result = bool(len(input_string) <= 0)
        return result

    def invalid_chars(self, input_string, allowed_chars):
        """Return boolean based on occurence of characters in 'input_string' in given array of characters."""
        for char in input_string:
            if not char in allowed_chars:
                return True
        return False

    def may_be_url(self, input_string, allowed_urls, should_be_file=False):
        """Return bool based on parsing of the given URL and comparing parts of it against a whitelist.

        Only links from defined whitelist are allowed.
        If should_be_file flag is set 'True', check if the link appears to direct to a lua-file or archive.
        """
        if '//' not in input_string:
            input_string = '%s%s' % ('http://', input_string)
        url_parse_result = urlparse(input_string)
        if should_be_file:
            for extension in self.allowed_file_ext:
                if url_parse_result.path.find(extension) > 0:
                    # found one of the expected file extensions in URL path
                    return True
            # none of the expected file extensions found in URL path
            return False
        else:
            for url in allowed_urls:
                if url in url_parse_result.netloc:
                    # netlocation is in whitelist, thus assume URL is safe
                    return True
            # If not hit in allowed urls, don't allow it
            return False

    #### Utility
    def validation_error(self, result, input_element, reason):
        """Modify a given result object to reflect a validation error that has happened and all necessary information to show the error to the user."""
        result['check'] = False
        if input_element not in result['error_field']:
            result['error_field'].append(input_element)
            result['error_reason'].append(reason)
            print('Validation failed because "'+reason+'".')
        return result

    def get_validation_type(self, element_id):
        """Return the validation type of a input element as substring from the given elements id."""
        validation_type = element_id.split('_')[1]
        return validation_type

    def get_mandatory(self, element_id):
        """Return boolean of test for certain substring in given string."""
        is_mandatory = bool(element_id.find('_req') >= 0)
        return is_mandatory

    #### Framework
    def static(self, foldername, filename):
        """Serve static files."""
        return static_file(filename, root='./'+foldername)

    def js_static(self, filename):
        """Serve static JS."""
        return static_file(filename, root='./js')

    def js_static_bootstrap(self, filename):
        """Serve static bootstrap JS modules."""
        return static_file(filename, root='./js/bootstrap')

    def img_static(self, filename):
        """Serve static image files."""
        return static_file(filename, root='./img')

    def css_static(self, filename):
        """Serve static css files."""
        return static_file(filename, root='./css')

    def fonts_static_bootstrap(self, filename):
        """Serve icon webfonts from bootstrap."""
        return static_file(filename, root='./fonts/bootstrap')

    def fonts_static(self, filename):
        """Serve webfonts."""
        return static_file(filename, root='./fonts')

    #### Actual Webform
    def show_form(self):
        """Return login form to the user."""
        return template('form', strings=self.strings)

    def process_form(self):
        """Process the login attempt of a user."""
        validation_result = self.validate_form(request.forms)
        if validation_result['check'] is True:
            # Success
            self.generate_modinfo(self.create_modinfo_object(request.forms))
            redirect('/?submit=success')
        else:
            # Validation Error
            return template('form', invalidation_field=validation_result['error_field'], invalidation_cause=validation_result['error_reason'], originalInput=request.forms, strings=self.strings)

    def get_file_from_url(self, url):
        """From an url containing a file, extract the filename. No validation is done."""
        result = urlparse(url).path.rsplit('/', 1)
        if len(result) == 2:
            return result[1]

    def create_modinfo_object(self, form):
        """From an pybottle form dictionary, create a normalized object."""
        modinfo_object = dict()
        modinfo_object['name'] = form.get('modname_text_req')
        modinfo_object['description'] = form.get('description_text_req')
        modinfo_object['author'] = form.get('author_text_req')
        modinfo_object['version'] = form.get('mod_version_version')
        modinfo_object['tested_version'] = form.get('game_version_version')
        modinfo_object['url'] = form.get('url_url')
        if form.get('package_bool') == 'on':
            package = form.get('package_name_text')
        else:
            package = ''
        modinfo_object['package'] = package
        modinfo_object['files'] = []
        for formelement in form:
            if 'file' in formelement:
                modinfo_object['files'].append({'url': form.get(formelement), 'file_name': self.get_file_from_url(form.get(formelement)), 'relative_path': form.get('gamepath_text')})
        return modinfo_object

    def generate_modinfo(self, modinfo_object):
        """Take a object with all necessary and optional fields to create a mod info file.

        The file can than be committed to the central mod repository, and be used to
        install the mod via the mod manager.
        """
        # Create directory for new mod
        try:
            newpath = '../mod-repository/'+modinfo_object['name'].replace(' ', '_').lower()
            os.mkdir(newpath)
        except OSError as e:
            print('Problem creating the mod\'s folder: '+str(e))
        except Exception as e:
            print('Generic problem: '+str(e))

        # Create modinfo file inside, containing the form input as json
        try:
            newfile = open(newpath + '/modinfo.json', mode='w+')
            simplejson.dump(modinfo_object, newfile)
            newfile.close()
        except Exception as e:
            print('Generic problem: '+str(e))

    #### Error pages
    def show_error_page(self, error_type):
        """Return generic error page based on error type."""
        return template('error', error_type=error_type, strings=self.strings)

    def error404(self, httperror):
        """Return 404 error page."""
        return self.show_error_page('404')

    def error500(self, httperror):
        """Return 500 error page."""
        return self.show_error_page('500')

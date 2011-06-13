#!/usr/bin/env python
# vim: tw=80 sw=4 et

import json
import os
import re
import sys
import textwrap
from string import Template

__author__    = 'Todd A. Jacobs'
__copyright__ = 'Copyright 2011, Todd A. Jacobs'
__license__   = "GPLv3"

class Programmer:
    """
    A demo class for consuming JSON data and using it to present a precis for a
    given programmer. The imagined use-case is converting RESTful data (perhaps
    from Rails or CouchDB) into a useful narrative format.
    """
    def __init__(self, filename=None):
        self.attributes=[]
        if filename == None: return
        self.attributes = self.load_file(filename)

    def load_file(self, json_filename):
        with open(json_filename) as f:
            return json.load(f)

    def insert_and_into_list_of_items(self, items):
        """
        A comma-separated list should have the word 'and' prepended to the last
        item.
        """
        return items.insert(-1, 'and')

    def join_items(self, items):
        return ', '.join(items)

    def remove_comma_after_conjunctions(self, string):
        return re.sub( '(and|or)[,]', '\\1', string )

    def present(self):
        """Present the JSON data in a narrative format."""
        # Parse the JSON into some useful chunks.
        programmer_info = self.attributes['programmer']
        qualifications = programmer_info['attributes']
        # Munge the programmer's qualifications in various ways to fit a more
        # narrative style.
        self.insert_and_into_list_of_items(qualifications)
        qualifications = self.join_items(qualifications)
        qualifications = self.remove_comma_after_conjunctions(qualifications)
        msg = Template( '$first_name $last_name currently works at ${company}. '
                        'You should consider hiring $first_name because of his '
                        'many sterling qualities. These include being '
                        '$qualifications.' )
        # This does some heavy lifting by populating the message template,
        # wrapping the resulting text at 80 characters, and then printing the
        # resulting wrapped paragraph.
        para = ( textwrap.fill( msg.safe_substitute( programmer_info,
                                                     qualifications=qualifications),
                                                     80 ))
        print(para)
        return para

if __name__ == '__main__':
    fixture_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'example_data.json')
    if len(sys.argv) > 1 and os.path.isfile( sys.argv[1] ):
        filename = sys.argv[1]
    elif os.path.isfile(fixture_file):
        filename = fixture_file
    else:
        sys.stderr.write('Fatal Error: No JSON file found.\n')
        sys.exit(1)
    p = Programmer(filename)
    p.present()

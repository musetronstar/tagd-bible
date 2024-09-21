'''
Reusable utility functions
'''

import sys
import os
import __main__ as main

def warn(*args, **kwargs):
    '''print to stderr'''
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)

def die(*args, **kwargs):
    '''print message to stderr and exit with err code 1'''
    warn(*args, **kwargs)
    sys.exit(1)

def program_name():
    '''return program name of running program'''
    return os.path.basename(main.__file__)

def file_string(fname):
    '''accepts a string filename and returns file contents as a string'''
    try:
        f = open(fname, 'rb')
    except OSError:
        die("failed to open file:", fname)
    with f:
        return f.read()


#!/usr/bin/python3

'''
Parse HTML documents to generate:
* tag heirarchy + attributes as URNs
* bibles as TAGL
'''

from mypyutils import warn, die, program_name, program_dir, file_string
import sys
import os
from bs4 import BeautifulSoup, Tag, NavigableString
import urllib.parse

def traverse_tag(tag, prefix=''):
    '''recursively visit each tag child'''
    prefix = f'{prefix}:{tag.name}' if prefix else tag.name
    urn = f'{prefix}:{urllib.parse.urlencode(tag.attrs)}'
    print(urn)
    for c in tag.contents:
        if isinstance(c, Tag):
            traverse_tag(c, prefix)
        elif isinstance(c, NavigableString):
            #s = c.string.strip()
            #if len(s):
            #    print(f'string({len(s)}):', s)
            pass

def html_parser(html_doc):
    '''return parser for WEB Bible HTML'''
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

# memoize tuple list
CACHE_WEB_SRCs = None
def WEB_SRCs(*type_codes):
    '''
    accept a variable length tuple of type codes

    return list of tuples:
        [(type-code, abs-path-to-html-file, title)...]

    example tuple:
        ('oo', '/path/to/tagd-bible/bibles/WEB/GEN01.html', 'Genesis')

    where type codes are:
        xx  Auxillary/Supplimental Documents
        oo  Old Testament
        aa  Apocrypha
        nn  New Testament
    '''
    global CACHE_WEB_SRCs 
    if not CACHE_WEB_SRCs:
        CACHE_WEB_SRCs = []
        tagd_bible_dir = os.path.split(program_dir())[0]
        srcs = tagd_bible_dir + '/bibles/WEB_SRCs.txt'
        srcs_dir = tagd_bible_dir + '/bibles/WEB'
        with open(srcs) as fi:
            for ln in fi:
                type_code, fname, title = ln.rstrip().split('\t')
                abs_path = f'{srcs_dir}/{fname}'
                CACHE_WEB_SRCs.append( (type_code, abs_path, title) )

    if len(type_codes):
        return [
            (type_code, abs_path, title)
            for type_code, abs_path, title in CACHE_WEB_SRCs
            if type_code in type_codes
        ]
    else:
        return CACHE_WEB_SRCs

def WEB_URNs(args):
    '''print WEB HTML tag heirarchy+attributes as URNs'''
    for type_code, path, title in WEB_SRCs('oo','nn', 'aa'):
        parser = html_parser(file_string(path))
        traverse_tag(parser.html)

# command handlers
CMDS = {
    'web-urns': WEB_URNs
}

if __name__ == '__main__':
    usage = f'usage: {program_name()} <WEB-URNs|WEB-TAGL> [args]'
    if len(sys.argv) < 2:
        die(usage) 
    cmd = sys.argv[1]
    if len(sys.argv) >= 3:
        args = sys.argv[2:]
    else:
        args = []
    handler = CMDS.get(cmd.lower(), None)
    if not handler:
        die(f'no such command: {cmd}\n{usage}')
    handler(args)

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

def print_tag_URN(tag, prefix):
    '''print tag heirarchy + attributes as URN'''
    print(prefix)

def tag_URN(tag, prefix):
    '''return tag heirarchy + attributes as URN'''
    prefix = f'{prefix}:{tag.name}' if prefix else tag.name
    if tag.name in ('html', 'body'):
        return prefix
    # prepare attributes by joining lists as CSV
    # generalize specific tags (e.g. verses) by removing ids, etc.
    for k, v in tag.attrs.items():
        if isinstance(v, list):
            tag.attrs[k] = ','.join(v)
        if k in ('id', 'href'):
            tag.attrs[k] = ''

    if len(tag.attrs):
        qs = urllib.parse.urlencode(tag.attrs, safe='/,').replace(',+', ',')
        prefix = f'{prefix}?{qs}'

    # every body tag will have the prefix, so ignore it
    #ignore = 'html:body:div?class=main'
    #if prefix.startswith(ignore):
    #    return prefix[len(ignore):]
    #else:
    #    return prefix

    return prefix

def traverse_tag(tag, tag_handler, string_handler, prefix=''):
    '''
    recursively visit each Tag child
    call tag_handler(Tag, prefix) on each Tag
    call string_handler(Tag, NavigableString, prefix) on each NavigableString
    '''
    prefix = tag_URN(tag, prefix)
    tag_handler(tag, prefix)
    for c in tag.contents:
        if isinstance(c, Tag):
            traverse_tag(c, tag_handler, string_handler, prefix)
        elif isinstance(c, NavigableString):
            string_handler(tag, c, prefix)

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
        srcs = tagd_bible_dir + '/docs/WEB_SRCs.txt'
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
        traverse_tag(parser.html, print_tag_URN, lambda t, s, p: None)

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

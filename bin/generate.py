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

def print_tag_URN(tag, src, prefix):
    '''print tag heirarchy + attributes as URN'''
    print(prefix)

def tag_URN(tag, src, prefix):
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

URN_data = {}
def append_URN_strings(tag, string, src, prefix):
    '''append NavigableString dictionary item having URN key'''
    global URN_data
    str_list = URN_data.get(prefix, [])
    if string:
        str_list.append(string)
    URN_data[prefix] = str_list

def traverse_tag(tag, tag_handler, string_handler, src, prefix=''):
    '''
    recursively visit each Tag child
    call tag_handler(Tag, src, prefix) on each Tag
    call string_handler(Tag, NavigableString, src, prefix) on each NavigableString

    Where src is a dictionary of WEB_src data
    '''
    prefix = tag_URN(tag, src, prefix)
    tag_handler(tag, src, prefix)
    for c in tag.contents:
        if isinstance(c, Tag):
            traverse_tag(c, tag_handler, string_handler, src, prefix)
        elif isinstance(c, NavigableString):
            string_handler(tag, c.strip(), src, prefix)

def html_parser(html_doc):
    '''return parser for WEB Bible HTML'''
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

# memoize tuple list
CACHE_WEB_srcs = None
def WEB_srcs(*type_codes):
    '''
    accept a variable length tuple of type codes

    return list of dictionaries (example):
        [
            {
                'order': '01',
                'type-code': 'oo',
                'title': 'Genesis',
                'index': '/path/to/tagd-bible/bibles/WEB/GEN.html',
                'srcs': ['/path/to/tagd-bible/bibles/WEB/GEN01.html' ...],
            }
            ...
        ]

    where type codes are:
        xx  Auxillary/Supplimental Documents
        oo  Old Testament
        aa  Apocrypha
        nn  New Testament
    '''
    global CACHE_WEB_srcs 

    def WEB_src_dict(order, type_code, title, index, srcs):
        '''accept row from WEB_src, return dictionary'''
        return {
            'order': order,
            'type-code': type_code,
            'title': title,
            'index': index,
            'srcs': srcs.split(' ')
        }

    if not CACHE_WEB_srcs:
        CACHE_WEB_srcs = []
        tagd_bible_dir = os.path.split(program_dir())[0]
        srcs = tagd_bible_dir + '/docs/WEB-src-indexes.tsv'
        srcs_dir = tagd_bible_dir + '/bibles/WEB'
        with open(srcs) as fi:
            for ln in fi:
                order, type_code, title, fname, srcs = ln.rstrip().split('\t')
                abs_path = f'{srcs_dir}/{fname}'
                CACHE_WEB_srcs.append(WEB_src_dict(order, type_code, title, abs_path, srcs))

    if len(type_codes):
        return [
            WEB_src_dict(order, type_code, title, abs_path, srcs)
            for order, type_code, title, abs_path, srcs in CACHE_WEB_srcs
            if type_code in type_codes
        ]
    else:
        return CACHE_WEB_srcs

def WEB_URNs(args):
    '''print WEB HTML tag heirarchy+attributes as URNs'''
    #empty_tag_handler = lambda t, d, p: None
    empty_string_handler = lambda t, s, d, p: None
    for d in WEB_srcs():
        parser = html_parser(file_string(d['index']))
        traverse_tag(parser.html, print_tag_URN, empty_string_handler, d)
        #traverse_tag(parser.html, empty_tag_handler, append_URN_strings, d)

    #global URN_data
    #from pprint import pprint
    #pprint(URN_data, width=160 )

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

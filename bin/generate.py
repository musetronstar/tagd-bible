#!/usr/bin/python3

'''
Parse HTML document and print tag heirarchy + attributes as URNs
'''

from mypyutils import warn, die, program_name, file_string
import sys
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

if __name__ == '__main__':
    prg = program_name()
    if len(sys.argv) < 2:
        die(f'usage: {prg} <html-file1> [html-filen...]') 
    fnames = sys.argv[1:]
    for f in fnames:
        parser = html_parser(file_string(f))
        traverse_tag(parser.html)

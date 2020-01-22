#!/usr/bin/env python

import argparse

from ssg.site import Site

import ssg.parsers

parser = argparse.ArgumentParser(prog='ssg', description='Static Site Generator')
parser.add_argument('--source', '-s', metavar='SOURCE', default=None, help='Content path')
parser.add_argument('--dest', '-d', metavar='DEST', default=None, help='Build path')

args = parser.parse_args()

config = {
    'parsers': [
        ssg.parsers.MarkdownParser(),
        ssg.parsers.ReStructuredTextParser(),
        ssg.parsers.ResourceParser(),
    ]
}
config['source'] = args.source or 'content'
config['dest'] = args.dest or 'dist'

Site(**config).build()

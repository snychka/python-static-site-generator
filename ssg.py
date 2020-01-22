#!/usr/bin/env python

import argparse

from ssg.site import Site

import ssg.parsers

parser = argparse.ArgumentParser(prog='ssg', description='Static Site Generator')
parser.add_argument('--source', '-s', metavar='SOURCE', default=None, help='Content path')
parser.add_argument('--dest', '-d', metavar='DEST', default=None, help='Build path')

args = parser.parse_args()

config = {
    'source': 'content',
    'dest': 'dist',
    'parsers': [
        ssg.parsers.MarkdownParser(),
        ssg.parsers.ResourceParser()
    ]
}

Site(**config).build()

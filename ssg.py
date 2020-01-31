#!/usr/bin/env python

import argparse

from ssg.site import Site

import ssg.parsers

parser = argparse.ArgumentParser(prog="ssg", description="Static Site Generator")
parser.add_argument(
    "--source", "-s", metavar="SOURCE", default="content", help="Content path"
)
parser.add_argument("--dest", "-d", metavar="DEST", default="dist", help="Build path")

args = parser.parse_args()

config = {
    "source": args.source,
    "dest": args.dest,
    "parsers": [
        ssg.parsers.MarkdownParser(),
        ssg.parsers.ReStructuredTextParser(),
        ssg.parsers.ResourceParser(),
    ],
}

Site(**config).build()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mkpreamble.py - Generate a tex preamble from metadata.bib

import sys
import argparse
import json
import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode


def load_bibtex(f):
    parser = BibTexParser()
    parser.alt_dict = {}

    with open(f, 'r') as fd:
        txt = re.sub('^\s*%.*$', '', fd.read(), flags=re.MULTILINE)
        bib = bibtexparser.loads(txt, parser=parser)

    return bib.entries


def getstr(d, key, default=None):
    val = d.get(key, None)
    if val != None and len(val.strip()) > 0: return val.strip()
    else:                                    return default


def getlist(d, key, sep=',\s*'):
    val = getstr(d, key)
    if val: return [a.strip() for a in re.split(sep, val)]
    else:   return []


def format_entry(pattern, *values):
    if all(values): return pattern % values
    else:           return ''


def format_command(name, content):
    return '\\newcommand{\\%s}{\n%s\n}' % (name, content)


def format_title(metadata):
    title = getstr(metadata, 'title', '')
    thanks = getstr(metadata, 'thanks')
    mrclass = getlist(metadata, 'mrclass')
    # TODO: keywords?

    L = [title]

    if thanks:
        L.append(r'\thanks{%s}' % thanks)

    if mrclass:
        L.append(r'  \unfootnote{\textbf{AMS CLassification:} %s.}' % (', '.join(mrclass)))

    return '\n'.join(L)


def format_authors(authors):
    # TODO: individual thanks
    return r' \and '.join([a['name'] for a in authors])


def format_date(metadata):
    date = metadata.get('date', None)
    if date:
        y, m, d = date.split('-')
        return r'\formatdate{%s}{%s}{%s}' % (d.strip(), m.strip(), y.strip())


def format_abstract(metadata):
    return metadata.get('abstract', '')


def format_authorlist(authors):
    L = []
    for a in authors:
        L.append(r'  \vspace{1em}')
        L.append(r'  \parbox[t]{0.5\textwidth}{')
        L.append(format_entry(r'    \textbf{%s}\\',       a.get('name',None)))
        L.append(format_entry(r'    \texttt{%s}\\',       a.get('email',None)))
        L.append(format_entry(r'    \texttt{\url{%s}}\\', a.get('web',None)))
        L.append(r'    \\')
        L.append(format_entry(r'    %s\\',                a.get('university',None)))
        L.append(format_entry(r'    %s\\',                a.get('department',None)))
        L.append(format_entry(r'    %s\\',                a.get('address',None)))
        L.append(format_entry(r'    %s\\',                a.get('city',None)))
        L.append('  }')

    return '\n'.join(L)


def format_preamble(metadata, authors):
    L = []
    L.append('% Auto-generated preamble')
    L.append(format_entry(r'\title{%s}', format_title(metadata)))
    L.append(format_entry(r'\author{%s}', format_authors(authors)))
    L.append(format_entry(r'\date{%s}', format_date(metadata)))
    L.append(format_command('makeabstract', format_abstract(metadata)))
    L.append(format_command('makeauthorlist', format_authorlist(authors)))
    return '\n\n'.join(L)


# ----------------------------------------------------------------------- #
# Argument parsing                                                        #
# ----------------------------------------------------------------------- #

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description='Generate preamble')

parser.add_argument("metadata", help="Metadata file",)

args = parser.parse_args()

entries = load_bibtex(args.metadata)
metadata = None
authors = []

for e in entries:
    if e['ENTRYTYPE'] == 'article':
        metadata = e

    elif e['ENTRYTYPE'] == 'misc':
        authors.append(e)

print(format_preamble(metadata, authors))

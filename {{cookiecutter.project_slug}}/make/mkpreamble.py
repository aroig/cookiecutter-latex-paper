#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) {{ cookiecutter.date.split('-')[0] }}, {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>
# All rights reserved.
{%- raw %}

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


def reindent(s, delta):
    if delta >= 0:
        return re.sub('^', delta * ' ', s, flags=re.MULTILINE)
    else:
        return re.sub('^' + (-delta) * ' ', '', s, flags=re.MULTILINE)


def format_entry(pattern, *values):
    if all(values):
        return pattern % values


def format_command(name, content):
    if content:
        if '\n' in content: return '\\%s{%%\n%s%%\n}' % (name, reindent(content, 2))
        else:               return '\\%s{%s}' % (name, content)


def format_environment(name, content):
    if content:
        return '\\begin{%s}\n%s\n\\end{%s}' % (name, reindent(content, 2), name)


def format_title(metadata):
    title = getstr(metadata, 'title', '')
    thanks = getstr(metadata, 'thanks')
    mrclass = getlist(metadata, 'mrclass')
    # TODO: keywords?

    L = [title]

    if thanks:
        L.append(r'\thanks{%s}' % thanks)

    if mrclass:
        L.append(r'\unfootnote{\textbf{AMS CLassification:} %s.}' % (', '.join(mrclass)))

    return '%\n'.join(L)


def format_authors(authors):
    L = []
    for a in authors:
        name = getstr(a, 'name')
        thanks = getstr(a, 'thanks')
        if thanks: L.append(name + format_command('thanks', thanks))
        else:      L.append(name)
    return r' \and '.join(L)


def format_date(metadata):
    date = getstr(metadata, 'date')
    if date:
        y, m, d = date.split('-')
        return r'\formatdate{%s}{%s}{%s}' % (d.strip(), m.strip(), y.strip())


def format_abstract(metadata):
    abstract = getstr(metadata, 'abstract')
    return format_environment("abstract", abstract)


def format_authorlist(authors):
    L = []
    for a in authors:
        L.append(r'  \vspace{1em}')
        L.append(r'  \parbox[t]{0.5\textwidth}{')
        L.append(format_entry(r'    \textbf{%s}\\',       a.get('name',None)))
        L.append(format_entry(r'    \texttt{%s}\\',       a.get('email',None)))
        L.append(format_entry(r'    \texttt{\url{%s}}\\', a.get('url',None)))
        L.append(r'    \\')
        L.append(format_entry(r'    %s\\',                a.get('university',None)))
        L.append(format_entry(r'    %s\\',                a.get('department',None)))
        L.append(format_entry(r'    %s\\',                a.get('address',None)))
        L.append(format_entry(r'    %s\\',                a.get('city',None)))
        L.append('  }')

    return '%\n'.join([it for it in L if it != None])


def format_preamble(metadata, authors):
    L = []
    L.append('% Auto-generated preamble')

    L.append(format_command('title', format_title(metadata)))
    L.append(format_command('author', format_authors(authors)))
    L.append(format_command('date', format_date(metadata)))

    # add institute entry for beamer slides
    if metadata['entrysubtype'] == 'slides':
        for a in authors:
            if a['name'] in metadata['author']:
                L.append(format_command('institute', a['university']))

    L.append(format_command(r'newcommand{\makeabstract}', format_abstract(metadata)))
    L.append(format_command(r'newcommand{\makeauthorlist}', format_authorlist(authors)))

    return '\n\n'.join([it for it in L if it != None])


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

{%- endraw %}

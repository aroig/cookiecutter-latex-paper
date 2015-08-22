#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mkpreamble.py - Generate a tex preamble from metadata.bib

import sys
import argparse
import json

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode


def load_bibtex(f):
    parser = BibTexParser()
    parser.alt_dict = {}

    with open(f, 'r') as fd:
        bib = bibtexparser.loads(fd.read(), parser=parser)

    return bib.entries


def print_entry(pattern, *values):
    if all(values):
        print(pattern % values)


def print_abstract(metadata):
    abstract = metadata.get('abstract',None)
    print('')
    print(r'\newcommand{\makeabstract}{')
    if abstract != None and len(abstract.strip()) > 0:
        print_entry('\\begin{abstract}\n%s\n\\end{abstract}', abstract)
    print(r'}')


def print_authorlist(authors):
    print("")
    print(r'\newcommand{\makeauthorlist}{')
    for a in authors:
        print(r'  \vspace{1em}')
        print(r'  \parbox[t]{0.5\textwidth}{')
        print_entry(r'    \textbf{%s}\\',       a.get('name',None))
        print_entry(r'    \texttt{%s}\\',       a.get('email',None))
        print_entry(r'    \texttt{\url{%s}}\\', a.get('web',None))
        print_entry(r'    %s\\',                a.get('university',None))
        print_entry(r'    %s\\',                a.get('department',None))
        print_entry(r'    %s\\',                a.get('address',None))
        print_entry(r'    %s\\',                a.get('city',None))
        print(r'  }')
    print(r'}')


def print_preamble(metadata, authors):
    print('% Auto-generated preamble')
    print('')
    print_entry(r'\title{%s}',          metadata.get('title',None))
    print_entry(r'\author{%s}',         metadata.get('author',None))
    print_entry(r'\date{%s}',           metadata.get('date',None))
    print_abstract(metadata)
    print_authorlist(authors)





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

print_preamble(metadata, authors)

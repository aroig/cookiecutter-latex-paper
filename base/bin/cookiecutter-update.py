#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import sys
import os
from cookiecutter.main import cookiecutter

TEMPLATE = sys.argv[1]
CONFIG   = sys.argv[2]
OUTDIR   = sys.argv[3]

extra_context = None
if os.path.exists(CONFIG):
    with open(CONFIG, 'r') as fd:
        extra_context = json.loads(fd.read())

cookiecutter(TEMPLATE,
             no_input=(extra_context != None),
             extra_context=extra_context,
             overwrite_if_exists=True,
             output_dir=OUTDIR)

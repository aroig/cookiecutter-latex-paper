#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Abdó Roig-Maranges <abdo.roig@gmail.com>
# All rights reserved.
#
# This file may be modified and distributed under the terms of the 3-clause BSD
# license. See the LICENSE file for details.

import os
import sys
import json
import shutil
import subprocess
from cookiecutter.main import cookiecutter


class TemporaryWorkdir():
    """Context Manager for a temporary working directory of a branch in a git repo"""

    def __init__(self, path, repo, branch='master'):
        self.repo = repo
        self.path = path
        self.branch = branch

    def __enter__(self):
        if not os.path.exists(os.path.join(self.repo, ".git")):
            raise Exception("Not a git repository: %s" % self.repo)

        if os.path.exists(self.path):
            raise Exception("Temporary directory already exists: %s" % self.path)

        os.makedirs(self.path)
        subprocess.run(["git", "worktree",  "add", "--no-checkout", self.path, self.branch],
                       cwd=self.repo)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
        subprocess.run(["git", "worktree", "prune"], cwd=self.repo)


def update_template(template_url, root, branch):
    """Update template branch from a template url"""
    tmpdir       = os.path.join(root, ".git", "cookiecutter")
    project_slug = os.path.basename(root)
    config_file  = os.path.join(root, ".cookiecutter.json")
    tmp_workdir  = os.path.join(tmpdir, project_slug)

    # read context from file.
    context = None
    if os.path.exists(config_file):
        with open(config_file, 'r') as fd:
            context = json.loads(fd.read())

    # create a template branch if necessary
    if subprocess.run(["git", "rev-parse", "-q", "--verify", branch], cwd=root).returncode != 0:
        firstref = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"],
                                  cwd=root,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True).stdout.strip()
        subprocess.run(["git", "branch", branch, firstref])

    with TemporaryWorkdir(tmp_workdir, repo=root, branch=branch):
        # update the template
        cookiecutter(template_url,
                     no_input=(context != None),
                     extra_context=context,
                     overwrite_if_exists=True,
                     output_dir=tmpdir)

        # commit to template branch
        subprocess.run(["git", "add", "-A", "."], cwd=tmp_workdir)
        subprocess.run(["git", "commit", "-m", "Update template"],
                       cwd=tmp_workdir)


if __name__ == '__main__':
    update_template(sys.argv[1], os.getcwd(), branch=sys.argv[2])

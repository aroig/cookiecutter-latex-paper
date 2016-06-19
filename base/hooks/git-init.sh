#!/usr/bin/bash

set -e

if [ ! -e ".git" ]; then
    git init
    git add -A
    git cm -m 'Initial commit'
    git branch "template"
fi

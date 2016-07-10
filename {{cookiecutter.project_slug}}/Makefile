# Copyright (c) {{ cookiecutter.date.split('-')[0] }}, {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>
# All rights reserved.
#
# This file is part of '{{ cookiecutter.project_name }}'.
#
# This file may be modified and distributed under the terms of the 3-clause BSD
# license. See the LICENSE file for details.

# shell settings
SHELL       := /usr/bin/bash
.SHELLFLAGS := -e -u -c

.ONESHELL:

# So we can use $$(variable) on the prerequisites, that expand at matching time.
.SECONDEXPANSION:


# URL for the source of the cookiecutter template
TEMPLATE_URL     := {{ cookiecutter._template }}




.PHONY: update-template

update-template:
	@python make/cookiecutter-update.py "$(TEMPLATE_URL)" template



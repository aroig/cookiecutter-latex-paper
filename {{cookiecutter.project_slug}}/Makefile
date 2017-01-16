# Copyright (c) {{ cookiecutter.date.split('-')[0] }}, {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>
# All rights reserved.
#
# This file is part of '{{ cookiecutter.project_name }}'.


# So that we can use newlines in recipes with $(\n)
define \n


endef

# Shell settings
SHELL       := /bin/bash
.SHELLFLAGS := -e -u -c

# Use a single shell
.ONESHELL:

# So we can use $$(variable) on the prerequisites, that expand at matching time.
.SECONDEXPANSION:



# -------------------------------------------------------------------------- #
# Source maintenance                                                         #
# -------------------------------------------------------------------------- #

.PHONY: update-template update-copyright

update-template:
	@python make/cookiecutter-update.py ".cookiecutter.json" template

update-copyright:
	@year=$$(date '+%Y')
	git ls-files | while read f; do
		sed -i "1,10{s/Copyright (c) \([0-9]\+\)\(-[0-9]\+\)\?,/Copyright (c) \1-$$year,/}" "$$f"
		sed -i "1,10{s/Copyright (c) $$year-$$year,/Copyright (c) $$year,/}" "$$f"
	done


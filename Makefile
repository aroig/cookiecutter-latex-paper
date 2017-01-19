# Copyright (c) 2016, Abdó Roig-Maranges <abdo.roig@gmail.com>
# All rights reserved.
#
# This file is part of 'LaTeX Base Cookiecutter'.


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


BUILD_DIR        := build
TESTPROJ_DIR     := $(BUILD_DIR)/testproj

all: build

.PHONY: build clean

## Build test project
build:
	@rm -Rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)
	cookiecutter --no-input -o $(BUILD_DIR) $(abspath .) project_slug=$(notdir $(TESTPROJ_DIR))
	rsync -a --exclude '.dummy' test/ $(TESTPROJ_DIR)

## Clean rendered test project
clean:
	@rm -Rf $(BUILD_DIR)


# -------------------------------------------------------------------------- #
# Source maintenance                                                         #
# -------------------------------------------------------------------------- #

.PHONY: update-template update-copyright

## Update cookiecutter template branch
update-template:
	@python make/cookiecutter-update.py ".cookiecutter.json" template

## Update copyright from file headers
update-copyright:
	@year=$$(date '+%Y')
	git ls-files | while read f; do
		sed -i "1,10{s/Copyright (c) \([0-9]\+\)\(-[0-9]\+\)\?,/Copyright (c) \1-$$year,/}" "$$f"
		sed -i "1,10{s/Copyright (c) $$year-$$year,/Copyright (c) $$year,/}" "$$f"
	done

.PHONY: help

## Print Makefile documentation
help:
	@perl -0 -nle 'printf("%-25s - %s\n", "$$2", "$$1") while m/^##\s*([^\r\n]+)\n^([\w-]+):[^=]/gm' \
		$(MAKEFILE_LIST) | sort
	printf "\n"
	perl -0 -nle 'printf("%-25s - %s\n", "$$2=", "$$1") while m/^##\s*([^\r\n]+)\n^([\w-]+)\s*:=/gm' \
		$(MAKEFILE_LIST) | sort


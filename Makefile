# Copyright (c) 2016, Abdó Roig-Maranges <abdo.roig@gmail.com>
# All rights reserved.
#
# This file is part of 'LaTeX Base Cookiecutter'.
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
TEMPLATE_URL     := local:cookiecutter-base

BUILD_DIR        := build


all: build

.PHONY: build clean

build:
	@rm -Rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)
	cookiecutter --no-input -o $(BUILD_DIR) $(abspath .)

clean:
	@rm -Rf $(BUILD_DIR)


.PHONY: update-template

update-template:
	@python make/cookiecutter-update.py "$(TEMPLATE_URL)" template

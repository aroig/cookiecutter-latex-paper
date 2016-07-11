# Copyright (c) 2016, Abdó Roig-Maranges <abdo.roig@gmail.com>
# All rights reserved.
#
# This file may be modified and distributed under the terms of the 3-clause BSD
# license. See the LICENSE file for details.

# shell settings
SHELL       := /usr/bin/bash
.SHELLFLAGS := -e -u -c

.ONESHELL:

# So we can use $$(variable) on the prerequisites, that expand at matching time.
.SECONDEXPANSION:


BUILD_DIR        := build


all: build

.PHONY: build clean

build:
	@rm -Rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)
	cookiecutter --no-input -o $(BUILD_DIR) $(abspath .)

clean:
	@rm -Rf $(BUILD_DIR)


.PHONY: update-template update-copyright

update-template:
	@python make/cookiecutter-update.py ".cookiecutter.json" template

update-copyright:
	@year=$$(date '+%Y')
	git ls-files | while read f; do
		sed -i "1,10{s/Copyright (c) \([0-9]\+\)\(-[0-9]\+\)\?,/Copyright (c) \1-$$year,/}" "$$f"
		sed -i "1,10{s/Copyright (c) $$year-$$year,/Copyright (c) $$year,/}" "$$f"
	done

